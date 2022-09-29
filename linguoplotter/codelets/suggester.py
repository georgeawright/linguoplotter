import math

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.nodes import Concept


class Suggester(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self._target_structures = target_structures
        self.confidence = 0.0

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        raise NotImplementedError

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        codelet = cls.make(parent_id, bubble_chamber, urgency=urgency)
        codelet.parent_concept = parent_concept
        return codelet

    @classmethod
    def get_follow_up_class(cls) -> type:
        raise NotImplementedError

    def run(self) -> CodeletResult:
        self.bubble_chamber.loggers["activity"].log_targets_dict(self)
        if not self._passes_preliminary_checks():
            self._decay_activations()
            self._fizzle()
            self.result = CodeletResult.FIZZLE
        else:
            self.bubble_chamber.loggers["activity"].log(
                self, "Preliminary checks passed"
            )
            self._calculate_confidence()
            self.bubble_chamber.loggers["activity"].log(
                self, f"Confidence: {self.confidence}"
            )
            self._boost_activations()
            self._engender_follow_up()
            self.result = CodeletResult.FINISH
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    @property
    def _parent_link(self):
        return self._structure_concept.relations_with(self._suggest_concept).get()

    @property
    def _suggest_concept(self):
        return self.bubble_chamber.concepts["suggest"]

    @property
    def _structure_concept(self):
        raise NotImplementedError

    @property
    def target_structures(self):
        return StructureCollection.union(
            self.bubble_chamber.new_structure_collection(
                *[
                    structure
                    for structure in self._target_structures.values()
                    if not isinstance(structure, StructureCollection)
                ]
            ),
            *[
                structure_collection
                for structure_collection in self._target_structures.values()
                if isinstance(structure_collection, StructureCollection)
            ],
        )

    def _boost_activations(self):
        self._suggest_concept.boost_activation(self.confidence)
        self._structure_concept.boost_activation(self.confidence)
        self._parent_link.boost_activation(self.confidence)
        self._suggest_concept.update_activation()
        self._structure_concept.update_activation()
        self._parent_link.update_activation()

    def _decay_activations(self):
        self._suggest_concept.decay_activation()
        self._parent_link.decay_activation()
        self._suggest_concept.update_activation()
        self._parent_link.update_activation()

    def _passes_preliminary_checks(self):
        raise NotImplementedError

    def _calculate_confidence(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        self.child_codelets.append(
            self.get_follow_up_class().spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.targets_dict,
                1 / (1 + math.e ** -(10 * self.confidence - 5)),
                # TODO: this should be a hyper-parameter
            )
        )

    def _fizzle(self):
        raise NotImplementedError
