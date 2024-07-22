import numpy as np
from utils.db_connector import DBConnector
import pandas as pd


class BaseResults:
    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0
        self.total = 0

    def set_result_values(self, tp: int, fp: int, tn: int, fn: int):
        self.tp = tp
        self.fp = fp
        self.tn = tn
        self.fn = fn
        self.total = self.tp + self.fp + self.tn + self.fn

    def get_accuracy(self):
        """
        Accuracy of the articles completed by this model.

        Accuracy = (TP + TN) / N
        """
        return (self.tp + self.tn) / self.total

    def get_precision(self):
        """
        Precision of the articles completed by this model.
        Precision = TP / (TP + FP)
        """
        return self.tp / (self.tp + self.fp)

    def get_recall(self):
        """
        Recall of the articles completed by this model.
        Recall = TP / (TP + FN)
        """
        return self.tp / (self.tp + self.fn)

    def get_f1_score(self):
        """
        The F1 score of the articles completed by this model.
        F1 = 2 * (Precision * Recall) / (Precision + Recall)
        """
        return (
            2
            * (self.get_precision() * self.get_recall())
            / (self.get_precision() + self.get_recall())
        )

    def get_specificity(self):
        """
        The specificity of the articles completed by this model.
        Specificity = TN / (TN + FP)
        """
        return self.tn / (self.tn + self.fp)

    def get_mcc(self):
        """
        The Matthews correlation coefficient of the articles completed by this model.
        MCC = (TP * TN - FP * FN) / SQRT((TP + FP)(TP + FN)(TN + FP)(TN + FN))
        """

        return (
            (self.tp * self.tn - self.fp * self.fn)
            / 2
            / (
                (self.tp + self.fp)
                * (self.tp + self.fn)
                * (self.tn + self.fp)
                * (self.tn + self.fn)
            )
            ** 0.5
        ) + 0.5

    def get_balanced_accuracy(self):
        """
        The balanced accuracy rate of the articles completed by this model.
        bAcc = (Recall + Specificity) / 2
        """
        return (self.get_recall() + self.get_specificity()) / 2

    def get_miss_rate(self):
        """
        The miss rate of the articles completed by this model.
        Miss Rate = FN / (FN + TP)
        """
        return self.fn / (self.fn + self.tp)

    def get_fb_score(self, beta: int = 1):
        """
        The F-beta score of the articles completed by this model.
        Fβ = (1 + β^2) * (Precision * Recall) / (β^2 * Precision + Recall)
        """
        return (
            (1 + beta**2)
            * (self.get_precision() * self.get_recall())
            / (beta**2 * self.get_precision() + self.get_recall())
        )

    def get_wss(self, recall: int = None):
        """
        The Work saved over sampling of the articles completed by this model, optionally at a specific recall.
        WSS = (TN + FN) / N − 1 + TP / ( TP + FN )
        If a fixed recall is specified, then the last term of the equation is replaced by it.
        """
        if recall is None:
            recall = self.get_recall()
        if recall >= 1:
            recall /= 100
        return (self.tn + self.fn) / self.total - 1 + recall

    def get_npv(self):
        """
        The negative predictive value of the articles completed by this model.
        NPV = TN / (TN + FN)
        """
        return self.tn / (self.tn + self.fn)

    def get_g_mean(self):
        """
        The geometric mean of the articles completed by this model.
        GMean = SQRT(Recall * Specificity)
        """
        return (self.get_recall() * self.get_specificity()) ** 0.5

    def get_gps(self):
        """
        The General Performance Score of the articles completed by this model.
        GPS = 2 * (Specificity * Recall) / (Specificity + Recall)
        """
        return (2 * self.get_specificity() * self.get_recall()) / (
            self.get_specificity() + self.get_recall()
        )

    def get_results(self):
        """
        Return all the results in a dictionary.
        """
        return {
            "completed_articles": self.get_completed(),
            "iterations": self.iterations,
            "articles_with_error": self.get_error(),
            "true_positive": self.tp,
            "false_positive": self.fp,
            "true_negative": self.tn,
            "false_negative": self.fn,
            "accuracy": "{:.4f}".format(self.get_accuracy()),
            "precision": "{:.4f}".format(self.get_precision()),
            "recall": "{:.4f}".format(self.get_recall()),
            "f1_score": "{:.4f}".format(self.get_f1_score()),
            "specificity": "{:.4f}".format(self.get_specificity()),
            "mcc": "{:.4f}".format(self.get_mcc()),
            "balanced_accuracy": "{:.4f}".format(self.get_balanced_accuracy()),
            "miss_rate": "{:.4f}".format(self.get_miss_rate()),
            "f2_score": "{:.4f}".format(self.get_fb_score(2)),
            "wss": "{:.4f}".format(self.get_wss()),
            "wss@95": "{:.4f}".format(self.get_wss(recall=0.95)),
            "npv": "{:.4f}".format(self.get_npv()),
            "g_mean": "{:.4f}".format(self.get_g_mean()),
            "general_performance_score": "{:.4f}".format(self.get_gps()),
        }

    def get_completed(self):
        """
        Get the number of completed articles.
        """
        return self.total

    def get_error(self):
        """
        Get the number of articles that errored.
        """
        raise NotImplementedError


class Results(BaseResults):
    def __init__(self, project_id: int):
        self.db_connector = DBConnector()
        self.project_id = project_id
        self.iterations = self.db_connector.get_project_iterations(self.project_id)
        self.moments = []
        super().__init__()
        for iter in range(self.iterations):
            print(iter)
            tp = self.db_connector.db.llmdecisions.count(
                where={"ProjectID": project_id, "Decision": "TP", "Iteration": iter}
            )
            fp = self.db_connector.db.llmdecisions.count(
                where={"ProjectID": project_id, "Decision": "FP", "Iteration": iter}
            )
            tn = self.db_connector.db.llmdecisions.count(
                where={"ProjectID": project_id, "Decision": "TN", "Iteration": iter}
            )
            fn = self.db_connector.db.llmdecisions.count(
                where={"ProjectID": project_id, "Decision": "FN", "Iteration": iter}
            )
            self.set_result_values(tp, fp, tn, fn)
            self.moments.append(self.get_results())

    def get_error(self):
        return self.db_connector.db.llmdecisions.count(
            where={"ProjectID": self.project_id, "Error": True}
        )

    def get_moment(self):
        """
        Get the moment of the model.
        """
        tmp = {}
        tmp["Metric"] = []
        tmp["mean"] = []
        tmp["std"] = []
        tmp["median"] = []
        tmp["IQR"] = []
        tmp["skewness"] = []
        tmp["kurtosis"] = []
        for k in self.get_moment_metric_names():
            data = [float(i[k]) for i in self.moments]
            tmp["Metric"].append(k)
            tmp["mean"].append(np.mean(data))
            tmp["std"].append(np.std(data))
            tmp["median"].append(np.median(data))
            tmp["IQR"].append(np.percentile(data, 75) - np.percentile(data, 25))
            tmp["skewness"].append(pd.Series(data).skew())
            tmp["kurtosis"].append(pd.Series(data).kurtosis())

        return pd.DataFrame(tmp)

    def get_moment_metric_names(self):
        return [
            "true_positive",
            "false_positive",
            "true_negative",
            "false_negative",
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "specificity",
            "mcc",
            "balanced_accuracy",
            "miss_rate",
            "f2_score",
            "wss",
            "wss@95",
            "npv",
            "g_mean",
            "general_performance_score",
        ]

    def get_results_metadata(self):
        return {
            "completed_articles": self.get_completed(),
            "iterations": self.iterations,
            "articles_with_error": self.get_error(),
            "true_positive": self.tp,
            "false_positive": self.fp,
            "true_negative": self.tn,
            "false_negative": self.fn,
        }

    def get_moment_values_df(self):
        return pd.DataFrame(self.moments)

    def get_kappa(self):
        """
        The Fleiss Kappa of the articles completed by this model.
        pi = (Include^2 + Exclude^2 - n) / (n * (n - 1))
        p_include = Sum(Include) / (n * N)
        p_exclude = Sum(Exclude) / (n * N)
        p_mean = pi.mean()
        p_e = p_include^2 + p_exclude^2
        kappa = (p_mean - p_e) / (1 - p_e)
        """

        # get include and exclude decisions
        article_keys = self.db_connector.db.llmdecisions.find_many(
            where={"ProjectID": self.project_id},
            distinct=["ArticleKey"],
        )
        unique_article_keys = [i.ArticleKey for i in article_keys]
        includes = self.db_connector.db.llmdecisions.group_by(
            by=["ArticleKey"],
            where={"ProjectID": self.project_id, "Decision": {"in": ["TP", "FP"]}},
            count=True,
        )

        excludes = self.db_connector.db.llmdecisions.group_by(
            by=["ArticleKey"],
            where={"ProjectID": self.project_id, "Decision": {"in": ["TN", "FN"]}},
            count=True,
        )
        include_dict = {
            include["ArticleKey"]: include["_count"]["_all"] for include in includes
        }
        exclude_dict = {
            exclude["ArticleKey"]: exclude["_count"]["_all"] for exclude in excludes
        }
        final_includes_counts = [
            include_dict.get(key, 0) for key in unique_article_keys
        ]
        final_excludes_counts = [
            exclude_dict.get(key, 0) for key in unique_article_keys
        ]
        N = len(unique_article_keys)
        n = self.iterations
        pi = (
            np.array(final_includes_counts) ** 2
            + np.array(final_excludes_counts) ** 2
            - n
        ) / (n * (n - 1))
        p_include = sum(final_includes_counts) / (n * N)
        p_exclude = sum(final_excludes_counts) / (n * N)
        p_mean = pi.mean()
        p_e = p_include**2 + p_exclude**2
        kappa = (p_mean - p_e) / (1 - p_e)
        return kappa
