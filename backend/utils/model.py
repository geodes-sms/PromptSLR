import os
import re
import pandas
import random
import openai
import nltk
from gensim.models import Word2Vec
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression as LR
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.model_selection import (
    RandomizedSearchCV,
    RepeatedStratifiedKFold,
    train_test_split,
    GridSearchCV,
)
from sklearn.metrics import (
    confusion_matrix,
    roc_curve,
    auc,
    fbeta_score,
    make_scorer,
    matthews_corrcoef,
)
from sklearn.pipeline import Pipeline
import joblib
import matplotlib.pyplot as plt
import numpy
import warnings

from backend.utils.output import ModelAnswer

# Ignore warnings from the grid search
warnings.filterwarnings("ignore")


class LanguageModel(object):
    def __init__(self, context="", parameters={}):
        """
        Context is the task of the LLM. Parameters are controlling the LLM.
        """
        self.model = None  # the actual model
        self.name = None
        self.context = context
        self.parameters = parameters

    def train(self, data):
        """
        Trains the model on the data which is used for training and validation.
        """
        raise NotImplementedError()

    def _api_decide(self, title, abstract, article_key=None):
        """
        Calls the API of the LLM.
        Returns a Decision object
        """
        raise NotImplementedError()

    def _set_answer(self, decision, article_project, article_key, article_decision):
        decision.project = article_project
        decision.key = article_key
        decision.correct_decision = article_decision
        # in case there is a punctuation or multiple words and all case must be upper to Match the ModelAnswer
        decision.answer = decision.answer.split(".")[0].split(",")[0].upper()
        if decision.answer.endswith("Error"):
            decision.finish_reason = decision.answer
            decision.answer = ModelAnswer(ModelAnswer.ERROR)
        else:
            decision.answer = ModelAnswer(decision.answer)

    def _process_decision(
        self, decision, article_project, article_key, article_decision
    ):
        self._set_answer(decision, article_project, article_key, article_decision)

    def _set_error_decision(self, decision):
        pass

    def decide(
        self,
        article=None,
        article_project=None,
        article_key=None,
        article_title=None,
        article_abstract=None,
    ):
        """
        Makes the decision and returns an instance of ModelAnswer.
        Pass the article or the project/key/title/abstract values directly.
        """
        try:
            # if article is not None:
            #     article_project = article["project"]
            #     article_key = article["key"]
            #     article_title = article["title"]
            #     article_abstract = article["abstract"]
            #     article_decision = article["decision"]
            decision = self._api_decide(article_title, article_abstract, article_key)
            # self._process_decision(
            #     decision, article_project, article_key, article_decision
            # )
        except Exception as e:
            print(e)
            # decision = Decision()
            # decision.project = article_project
            # decision.key = article_key
            # decision.correct_decision = article_decision
            # decision.answer = ModelAnswer(ModelAnswer.ERROR)
            # decision.finish_reason = str(type(e).__name__)
            # self._set_error_decision(decision)
        return decision


class TrainableModel(LanguageModel):
    grid_param_prefix = "classifier__"

    def __init__(self, context="", parameters={}, vectorizer_parameters={}):
        """
        This is a model that needs to be trained before it can make a decision.
        context is a sentence related to the topic of the systematic review that should be added to features (on top of title and abstract).
        Parameters are the paramters of the model. Refer to the API documentation of the model to set the correct parameters, they are passed as is.
        vectorizer_paramters are for the vectorizer Word2Vec, see https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.Word2Vec.
        min_count is set to ignore words with occurence less than 3 by default.
        workers is set to 4 threads by default.
        """
        super().__init__(context, parameters)
        self.training_parameters = {}
        if "min_count" not in vectorizer_parameters.keys():
            vectorizer_parameters["min_count"] = 3
        if "workers" not in vectorizer_parameters.keys():
            vectorizer_parameters["workers"] = 4
        self.vectorizer = Word2Vec(**vectorizer_parameters)
        self.threshold = 0
        self.seed = 0
        self.grid = {}
        self.folds = []
        self.decisions = {}

    def __preprocess(self, text):
        """
        Standardize the text
        """
        # text = str(text.encode("latin-1"), encoding="latin-1", errors="ignore")
        text = "".join([*filter(str.isascii, text)])
        # Remove special characters
        text = re.sub(r"[^a-zA-Z0-9\s]", r"", text)
        # Fix for invalid continuation byte
        text = text.lower()  # Convert to lowercase
        return text

    def save(self, path, filename):
        """
        Save the trained model and vectorizer to a path (no filename).
        """
        joblib.dump(self.vectorizer, os.path.join(path, f"{filename}_word2vec.bin"))
        return joblib.dump(self.model, os.path.join(path, f"{filename}.bin"))[0]

    def load(self, path, filename, vectorizer=True):
        """
        Load a pre-trained model from a path (no filename).
        """
        self.model = joblib.load(os.path.join(path, f"{filename}.bin"))
        if vectorizer:
            # Don't forget to load the pre-trained vectorizer too
            self.vectorizer = joblib.load(
                os.path.join(path, f"{filename}_word2vec.bin")
            )
        self.threshold = self.model.threshold

    def train(
        self,
        data,
        training_parameters={},
        print_roc=False,
        show_roc_plot=False,
        do_random_search=False,
    ):
        """
        Train the model and create a dictionary of all the decision. Each decision is identified by the article key and stores the decision and the parameters of the classifier that was tuned in this fold.
        If no dataset is provided, it will train it on filename.
        training_dataset is a CSV file with a header line and at least the columns title, abstract, and decision. If None, it will use the loaded dataset as training.
        training_parameters is the parameters of the training phase. Currently supported are:
            - seed: the seed of the random shuffling of the traning data. Default is 0.
            - fold_count: the number of folds indicating in how many times will the dataset be split for cross-validation. Default is 5.
            - epoch: the number of times each article is processed. Default is 10.
        print_roc prints the AUC and best threshold.
        show_roc_plot display the ROC graph.
        do_random_search specifies to use Random search instead of Grid search to save time.
        """
        # Set the training parameters
        self.seed = (
            training_parameters["seed"] if "seed" in training_parameters.keys() else 0
        )
        self.fold_count = (
            training_parameters["fold_count"]
            if "fold_count" in training_parameters.keys()
            else 5
        )
        self.epoch = (
            training_parameters["epoch"]
            if "epoch" in training_parameters.keys()
            else 10
        )
        # Preprocess the data
        data = pandas.read_csv(data, delimiter="\t")
        data.dropna(
            subset=["abstract"], inplace=True
        )  # ignore rows with missing abstracts
        context = self.__preprocess(self.context)
        data["title"] = data["title"].apply(self.__preprocess)
        data["abstract"] = data["abstract"].apply(self.__preprocess)
        data["article"] = data["title"] + "\n" + data["abstract"] + "\n" + context
        # Train word2vec model on the documents
        self.vectorizer.build_vocab(
            [nltk.word_tokenize(article) for article in data["article"]]
        )
        # Convert text to Word2Vec embeddings
        articles = numpy.array(
            [
                numpy.mean(
                    [
                        self.vectorizer.wv[word]
                        for word in article.split()
                        if word in self.vectorizer.wv.key_to_index
                    ],
                    axis=0,
                )
                for article in data["article"]
            ]
        )
        # Convert decision column to binary labels
        label_encoder = preprocessing.LabelEncoder()
        decisions = label_encoder.fit_transform(data["decision"])
        # decisions = data["decision"].apply(
        #    lambda x: 1 if x == CorrectAnswer.INCLUDE else 0
        # )
        ###
        # Train the model
        ###

        # Create the pipeline with data normalization
        pipeline = Pipeline(
            [("scaler", preprocessing.MinMaxScaler()), ("classifier", self.model)]
        )

        # Prefix the grid parameters because we use a pipeline
        self.grid = {
            TrainableModel.grid_param_prefix + k: v for k, v in self.grid.items()
        }

        # Set up the repeated stratified k-fold cross-validation because the datasets are small and imbalanced
        cv = RepeatedStratifiedKFold(
            n_splits=self.fold_count, n_repeats=self.epoch, random_state=self.seed
        )

        if do_random_search:
            search_strategy = RandomizedSearchCV
        else:
            search_strategy = GridSearchCV

        # This will be used as the key when storing each decision
        article_keys = data["key"].values.tolist()

        # Iterate over the cross-validation splits
        for train_index, test_index in cv.split(articles, decisions):
            train_articles, test_articles = articles[train_index], articles[test_index]
            train_decisions, test_decisions = (
                decisions[train_index],
                decisions[test_index],
            )

            # Fine-tune the model to find the best hyperparameters
            search = search_strategy(
                pipeline,
                self.grid,
                scoring=make_scorer(matthews_corrcoef),
                refit=True,
                cv=5,
                n_jobs=10,
            )
            search.fit(train_articles, train_decisions)

            # Set the best parameters from the search
            self.model = search.best_estimator_
            # Set the best parameters to the model, but remove the prefix in the keys
            self.parameters = {
                k[len(TrainableModel.grid_param_prefix) :]: v
                for k, v in search.best_params_.items()
            }

            # Make predictions on the test articles
            predicted_decisions = self.model.predict_proba(test_articles)[:, 1]

            # Compute the MCC score for different thresholds
            thresholds = numpy.linspace(0, 1, num=100)
            mcc_scores_for_thresholds = []
            for threshold in thresholds:
                decision_pred = (predicted_decisions >= threshold).astype(int)
                mcc = matthews_corrcoef(test_decisions, decision_pred)
                mcc_scores_for_thresholds.append(mcc)
            # Find the threshold that maximizes the MCC score
            best_threshold = thresholds[numpy.argmax(mcc_scores_for_thresholds)]
            if self.threshold == 0:
                self.threshold = best_threshold
            # Set the best threshold to make decisions
            self.model.threshold = self.threshold

            # Apply the learned threshold to convert probabilities to binary decisions
            decision_pred = (predicted_decisions >= self.threshold).astype(int)

            fold = {
                "model": search.best_estimator_["classifier"],
                "parameters": {
                    k[len(TrainableModel.grid_param_prefix) :]: v
                    for k, v in search.best_params_.items()
                },
                "articles": [article_keys[i] for i in test_index],
                "decisions": dict(
                    zip([article_keys[i] for i in test_index], decision_pred)
                ),
                "mcc": matthews_corrcoef(test_decisions, decision_pred),
                "confusion_matrix": confusion_matrix(
                    test_decisions, decision_pred
                ).ravel(),  # (TN, FP, FN, TP)
            }
            self.folds.append(fold)

            # What follows is not needed anymore
            fpr, tpr, thresholds = roc_curve(test_decisions, predicted_decisions)
            roc_auc = auc(fpr, tpr)
            if print_roc:
                print(
                    """
Best threashold = {}
Area under the curve = {}
""".format(
                        best_threshold, roc_auc
                    )
                )
            if show_roc_plot:
                # Plot the ROC curve
                plt.plot(fpr, tpr, color="blue", label="AUC = %0.2f" % roc_auc)
                plt.plot([0, 1], [0, 1], color="black", linestyle="--")
                plt.xlabel("False Positive Rate")
                plt.ylabel("True Positive Rate")
                plt.title("ROC Curve for Article Screening")
                plt.legend(loc="lower right")
                plt.show()

        for fold in self.folds:
            for k in fold["decisions"]:
                if k in self.decisions:
                    self.decisions[k].append((fold["decisions"][k], fold["parameters"]))
                else:
                    self.decisions[k] = [(fold["decisions"][k], fold["parameters"])]

    def _process_decision(
        self, decision, article_project, article_key, article_decision
    ):
        for d in decision:
            self._set_answer(d, article_project, article_key, article_decision)

    def _set_error_decision(self, decision):
        decision = [decision]

    def _api_decide(self, title, abstract, article_key=None):
        decisions = []
        if article_key not in self.decisions:
            d = Decision()
            d.answer = (
                ModelAnswer.ERROR
            )  # in case the article was never tested during cross-validation
            d.finish_reason = "article not found"
            return [d]
        for answer, param in self.decisions[article_key]:
            d = Decision()
            d.answer = ModelAnswer.INCLUDE if answer else ModelAnswer.EXCLUDE
            d.parameters = param
            decisions.append(d)
        return decisions


#########################
# Random
#########################
class Random(LanguageModel):
    def __init__(self, context="", parameters={}):
        """
        Context is ignored. Paramters should have the seed.
        """
        super().__init__(context, parameters)
        self.name = "random"
        self.seed = parameters["seed"]
        random.seed(self.seed)  # repeatable random

    def _api_decide(self, title, abstract, article_key=None):
        d = Decision()
        d.answer = random.choice([ModelAnswer.INCLUDE, ModelAnswer.EXCLUDE])
        d.parameters = self.seed
        return d


#########################
# GPT-3
#########################
class ChatGPT(LanguageModel):
    def __init__(self, context="", parameters={}, *args, **kwargs):
        """
        Context is the system prompt. Paramters should have the api_key, temperature, and max_tokens.
        """
        super().__init__(context, parameters)
        openai.api_key = self.parameters["api_key"]
        self.name = "gpt-3.5-turbo-0613"

    def api_decide(self, content, article_key=None):
        conversation = [
            {"role": "system", "content": self.context},
            {
                "role": "user",
                "content": content,
            },
        ]
        try:
            response = openai.ChatCompletion.create(
                model=self.name,
                messages=conversation,
                temperature=self.parameters["temperature"],
                max_tokens=self.parameters["max_tokens"],
            )
            return response
            # d.tokens = tokens = response["usage"]["total_tokens"]
            # d.answer = response.choices[0].message.content
            # finish_reason = response.choices[0].finish_reason
            # if finish_reason == "stop":  # otherwise there is an error
            #     finish_reason = ""
            # d.finish_reason = finish_reason
            # d.parameters = [
            #     f"{k}: {v}" for k, v in self.parameters.items() if k != "api_key"
            # ]  # all but the API Key
        except Exception as e:
            print(e)
            # d.answer = str(type(e).__name__)
        # return d


#########################
# llamafile
#########################
class LlamaFile(LanguageModel):
    def __init__(self, context="", parameters={}):
        pass


#########################
# Logistic Regression
#########################
class LogisticRegression(TrainableModel):
    def __init__(self, context="", parameters={}, vectorizer_parameters={}):
        """
        For the full list of parameters, see https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html.
        """
        super().__init__(context, parameters, vectorizer_parameters)
        self.model = LR()
        self.name = "logistic-regression"
        self.model.set_params(**(parameters if parameters is not None else {}))
        self.grid = {
            "penalty": [None, "l2", "elasticnet"],
            "C": numpy.logspace(-3, 3, 7),
            "solver": [
                "lbfgs",
                "liblinear",
                "newton-cg",
                "newton-cholesky",
                "sag",
                "saga",
            ],
        }


#########################
# C-Support Vector Classification
#########################
class SupportVectorMachine(TrainableModel):
    def __init__(self, context="", parameters={}, vectorizer_parameters={}):
        """
        For the full list of parameters, see https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html.
        """
        super().__init__(context, parameters, vectorizer_parameters)
        self.model = SVC(probability=True)
        self.name = "SVC"
        self.model.set_params(**(parameters if parameters is not None else {}))
        self.grid = {
            "kernel": ["linear", "poly", "rbf", "sigmoid"],
            "C": numpy.logspace(-3, 3, 7),
            "gamma": ["auto", "scale"] + numpy.logspace(-3, 3, 7).tolist(),
        }


#########################
# Multinomial Naive Bayes
#########################
class MultiNaiveBayes(TrainableModel):
    def __init__(self, context="", parameters={}, vectorizer_parameters={}):
        """
        For the full list of parameters, see https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html.
        """
        super().__init__(context, parameters, vectorizer_parameters)
        self.model = MultinomialNB()
        self.name = "MultinomialNaiveBayes"
        self.model.set_params(**(parameters if parameters is not None else {}))
        self.grid = {"alpha": numpy.logspace(-3, 3, 7), "fit_prior": [True, False]}


#########################
# Complement Naive Bayes
#########################
class ComplementNaiveBayes(TrainableModel):
    def __init__(self, context="", parameters={}, vectorizer_parameters={}):
        """
        For the full list of parameters, see https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.ComplementNB.html.
        """
        super().__init__(context, parameters, vectorizer_parameters)
        self.model = ComplementNB()
        self.name = "ComplementNaiveBayes"
        self.model.set_params(**(parameters if parameters is not None else {}))
        self.grid = {
            "alpha": numpy.logspace(-3, 3, 7),
        }


#########################
# Random Forest
#########################
class RandomForest(TrainableModel):
    def __init__(self, context="", parameters={}, vectorizer_parameters={}):
        """
        For the full list of parameters, see https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html.
        """
        super().__init__(context, parameters, vectorizer_parameters)
        self.model = RF()
        self.name = "RandomForest"
        self.model.set_params(**(parameters if parameters is not None else {}))
        self.grid = {
            "max_depth": [80, 90, 100, 110],
            "max_features": [2, 3],
            "min_samples_leaf": [3, 4, 5],
            "min_samples_split": [8, 10, 12],
            "n_estimators": [100, 200, 300, 1000],
        }
