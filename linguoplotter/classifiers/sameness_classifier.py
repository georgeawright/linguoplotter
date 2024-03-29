from linguoplotter import fuzzy
from linguoplotter.classifier import Classifier
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collections import StructureSet


class SamenessClassifier(Classifier):
    def classify(self, **kwargs: dict) -> FloatBetweenOneAndZero:
        """
        Required: ('start' AND 'end') OR 'collection'
        Optional: 'space', 'spaces'
        """
        start = kwargs.get("start")
        end = kwargs.get("end")
        collection = kwargs.get("collection")
        spaces = kwargs.get("spaces")
        space = kwargs.get("space")
        return_nan = kwargs.get("return_nan", False)

        collection = list(collection) if collection is not None else [start, end]
        if spaces is None:
            spaces = (
                StructureSet.union(
                    *[
                        item.parent_spaces.where(
                            is_conceptual_space=True, is_basic_level=True
                        )
                        for item in collection
                    ]
                )
                if space is None
                else [space]
            )
        distinct_pairs = [
            (collection[i], collection[j])
            for i in range(len(collection))
            for j in range(len(collection[:i]))
        ]
        if distinct_pairs == []:
            distinct_pairs = [(collection[0], collection[1])]
        if distinct_pairs[0][0].is_link:
            if end.parent_concept.subsumes(start.parent_concept):
                return 1.0
            if (
                start.parent_concept.is_compound_concept
                and end.parent_concept == start.parent_concept.args[0]
            ):
                return 0.0
            start_concept = (
                start.parent_concept
                if not start.parent_concept.is_slot
                else start.parent_concept.non_slot_value
            )
            end_concept = (
                end.parent_concept
                if not end.parent_concept.is_slot
                else end.parent_concept.non_slot_value
            )
            if start_concept == end_concept:
                return 1.0
        if distinct_pairs[0][0].is_label:
            return fuzzy.AND(
                start_concept.classifier.classify(
                    concept=start_concept, start=end.start, return_nan=return_nan
                )
                if start_concept is not None
                else 1.0,
                end_concept.classifier.classify(
                    concept=end_concept, start=start.start, return_nan=return_nan
                )
                if end_concept is not None
                else 1.0,
            )
        if distinct_pairs[0][0].is_relation:
            return fuzzy.AND(
                start_concept.classifier.classify(
                    concept=start_concept,
                    space=space,
                    start=end.start,
                    end=end.end,
                    return_nan=return_nan,
                )
                if start_concept is not None
                else 1.0,
                end_concept.classifier.classify(
                    concept=end_concept,
                    space=space,
                    start=start.start,
                    end=start.end,
                    return_nan=return_nan,
                )
                if end_concept is not None
                else 1.0,
            )
        return fuzzy.OR(
            *[
                fuzzy.AND(
                    *[
                        space.adjacency_of(pair[0], pair[1], return_nan=return_nan)
                        if pair[0].has_location_in_space(space)
                        and pair[1].has_location_in_space(space)
                        else 0.0
                        for pair in distinct_pairs
                    ]
                )
                for space in spaces
            ]
        )
