from utils.db_connector import DBConnector


class Results:
    def __init__(self, project_id: str):
        self.db_connector = DBConnector()
        self.project_id = project_id
        self.tp = self.db_connector.db.llmdecisions.count(
            where={"ProjectID": self.project_id, "Decision": "TP"}
        )
        self.fp = self.db_connector.db.llmdecisions.count(
            where={"ProjectID": self.project_id, "Decision": "FP"}
        )
        self.tn = self.db_connector.db.llmdecisions.count(
            where={"ProjectID": self.project_id, "Decision": "TN"}
        )
        self.fn = self.db_connector.db.llmdecisions.count(
            where={"ProjectID": self.project_id, "Decision": "FN"}
        )
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

    def get_results(self):
        """
        Return all the results in a dictionary.
        """
        return {
            "completed_articles": self.get_completed(),
            "articles_with_error": self.get_error(),
            "true_positive": self.tp,
            "false_positive": self.fp,
            "true_negative": self.tn,
            "false_negative": self.fn,
            "accuracy": self.get_accuracy(),
            "precision": self.get_precision(),
            "recall": self.get_recall(),
            "f1_score": self.get_f1_score(),
            "specificity": self.get_specificity(),
            "mcc": self.get_mcc(),
            "balanced_accuracy": self.get_balanced_accuracy(),
            "miss_rate": self.get_miss_rate(),
            "fb_score": self.get_fb_score(2),
            "wss": self.get_wss(),
            "wss@95": self.get_wss(95),
            "npv": self.get_npv(),
            "g_mean": self.get_g_mean(),
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
        return self.db_connector.db.llmdecisions.count(
            where={"ProjectID": self.project_id, "Error": True}
        )


class TrainableResults(Results):
    def __init__(self, project_id: str):
        super().__init__(project_id)
