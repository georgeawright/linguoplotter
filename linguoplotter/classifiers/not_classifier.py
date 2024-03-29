import math
from typing import List

from linguoplotter.classifier import Classifier


class NotClassifier(Classifier):
    def __init__(self, negated_concepts: List["Concept"]):
        self.negated_concept = (
            negated_concepts[0] if negated_concepts is not None else None
        )

    def classify(self, **kwargs: dict):
        return_nan = kwargs.get("return_nan", False)

        try:
            if kwargs["start"].is_slot:
                return 1.0
            if kwargs["end"].is_slot:
                return 1.0
        except KeyError:
            pass

        kwargs["return_nan"] = True
        positive_classification = self.negated_concept.classifier.classify(**kwargs)

        if math.isnan(positive_classification):
            return positive_classification if return_nan else 1.0
        return 1 - positive_classification
