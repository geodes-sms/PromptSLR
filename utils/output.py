import json
import re


class CorrectAnswer:
    """
    The ground truth decision.
    """

    INCLUDE = "Included"
    EXCLUDE = "Excluded"
    CONFLICT_INCLUDE = "ConflictIncluded"
    CONFLICT_EXCLUDE = "ConflictExcluded"

    def __init__(self, answer):
        self.answer = answer
        assert answer in (
            CorrectAnswer.INCLUDE,
            CorrectAnswer.EXCLUDE,
            CorrectAnswer.CONFLICT_INCLUDE,
            CorrectAnswer.CONFLICT_EXCLUDE,
        )

    def is_include(self):
        return self.answer in (CorrectAnswer.INCLUDE, CorrectAnswer.CONFLICT_INCLUDE)

    def is_exclude(self):
        return self.answer in (CorrectAnswer.EXCLUDE, CorrectAnswer.CONFLICT_EXCLUDE)

    def is_conflict(self):
        """
        The answer is was the result of a conflict resolution.
        """
        return self.answer in (CorrectAnswer.INCLUDE, CorrectAnswer.CONFLICT_EXCLUDE)

    def is_conflict_resolved(self):
        """
        The answer is was the result of a conflict resolution.
        """
        return self.answer in (CorrectAnswer.INCLUDE, CorrectAnswer.CONFLICT_EXCLUDE)


class ModelAnswer:
    """
    Decision made by the AI chatbot.
    """

    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"
    UNKOWN = "UNKOWN"  # in case it does not know what to decide
    MAYBE_INCLUDE = (
        "MAYBE_INCLUDE"  # in case it wants to include but not sure of including it.
    )
    MAYBE_EXCLUDE = (
        "MAYBE_EXCLUDE"  # in case it wants to exclude but not sure of excluding it.
    )
    ERROR = "ERROR"  # in case an error occurred when deciding for this article

    def __init__(self, answer, trainable=False):
        self.answer = answer
        self.trainable = trainable
        if trainable:
            assert answer in (
                CorrectAnswer.INCLUDE,
                CorrectAnswer.EXCLUDE,
                CorrectAnswer.CONFLICT_INCLUDE,
                CorrectAnswer.CONFLICT_EXCLUDE,
            )
        else:
            assert answer in (
                ModelAnswer.INCLUDE,
                ModelAnswer.MAYBE_INCLUDE,
                ModelAnswer.EXCLUDE,
                ModelAnswer.MAYBE_EXCLUDE,
                ModelAnswer.UNKOWN,
                ModelAnswer.ERROR,
            )

    def is_include(self):

        return (
            self.answer == ModelAnswer.INCLUDE
            if not self.trainable
            else self.answer
            in (
                CorrectAnswer.INCLUDE,
                CorrectAnswer.CONFLICT_INCLUDE,
            )
        )

    def is_exclude(self):
        return (
            self.answer == ModelAnswer.EXCLUDE
            if not self.trainable
            else self.answer
            in (
                CorrectAnswer.EXCLUDE,
                CorrectAnswer.CONFLICT_EXCLUDE,
            )
        )

    def is_conflict(self):
        """
        The answer is inconclusive.
        """
        return (
            self.answer in (ModelAnswer.MAYBE_INCLUDE, ModelAnswer.MAYBE_EXCLUDE)
            if not self.trainable
            else self.answer
            in (
                CorrectAnswer.CONFLICT_INCLUDE,
                CorrectAnswer.CONFLICT_EXCLUDE,
            )
        )

    def is_error(self):
        return self.answer == ModelAnswer.ERROR if not self.trainable else False


class Result:
    """
    The correctness of the decision w.r.t. the ground truth.
    """

    TRUE_POSITIVE = "TP"  # correctly included
    TRUE_NEGATIVE = "TN"  # correctly excluded
    FALSE_POSITIVE = "FP"  # incorrectly included
    FALSE_NEGATIVE = "FN"  # incorrectly excluded
    UNKNOWN = (
        "UK"  # unknown because answer is MAYBE, ERROR, or correct answer is CONFLICT
    )


class Output(ModelAnswer):
    def __init__(self, raw_output: str, trainable: bool = False):
        if trainable:
            self.answer = raw_output
            self.reason = None
            self.confidence = None
            super().__init__(self.answer, trainable=True)
        else:
            self.filter_string = re.compile(
                r'\{\s*"decision":\s*"([^"]+)"'
                r'(?:\s*,\s*"reason":\s*"([^"]*)")?'
                r'(?:\s*,\s*"confidence":\s*(\d+))?'
                r"\s*\}"
            )
            self.raw_output = raw_output
            self.parse()
            super().__init__(self.answer, trainable=False)

    def parse(self):
        try:
            res = self.filter_string.search(self.raw_output)
            if res:
                result = {
                    "decision": res.group(1),
                }
                if res.group(2) is not None:
                    result["reason"] = res.group(2)
                if res.group(3) is not None:
                    result["confidence"] = int(res.group(3))
                print(result)
                self.answer = result["decision"]
                self.reason = result["reason"] if "reason" in result else None
                self.confidence = (
                    result["confidence"] if "confidence" in result else None
                )
            else:
                self.answer = self.raw_output
                self.reason = None
                self.confidence = None
        except AttributeError:
            self.answer = self.raw_output
            self.reason = None
            self.confidence = None

    def get_decision(self, correct_answer: CorrectAnswer):
        if self.is_include() and correct_answer.is_include():
            return Result.TRUE_POSITIVE
        elif self.is_exclude() and correct_answer.is_exclude():
            return Result.TRUE_NEGATIVE
        elif self.is_include() and correct_answer.is_exclude():
            return Result.FALSE_POSITIVE
        elif self.is_exclude() and correct_answer.is_include():
            return Result.FALSE_NEGATIVE
        elif self.is_conflict():
            return Result.UNKNOWN
