from typing import Dict

from .bubble_chamber import BubbleChamber
from .codelets.suggesters import ChunkSuggester
from .coderack import Coderack
from .errors import NoMoreCodelets
from .hyper_parameters import HyperParameters
from .id import ID
from .interpreter import Interpreter
from .logger import Logger


class Linguoplotter:
    CODELET_RUN_LIMIT = HyperParameters.CODELET_RUN_LIMIT
    NUMBER_OF_START_CHUNK_SUGGESTERS = HyperParameters.NUMBER_OF_START_CHUNK_SUGGESTERS

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        coderack: Coderack,
        interpreter: Interpreter,
        loggers: Dict[str, Logger],
        activation_update_frequency: int = HyperParameters.ACTIVATION_UPDATE_FREQUENCY,
    ):
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack
        self.interpreter = interpreter
        self.loggers = loggers
        self.activation_update_frequency = activation_update_frequency

    @classmethod
    def setup(cls, loggers: Dict[str, Logger], random_seed: int = None):
        ID.reset()
        bubble_chamber = BubbleChamber.setup(loggers, random_seed=random_seed)
        coderack = Coderack.setup(bubble_chamber, loggers)
        loggers["structure"].coderack = coderack
        interpreter = Interpreter(bubble_chamber)
        return cls(bubble_chamber, coderack, interpreter, loggers)

    def run_program(self, program: str):
        self.interpreter.interpret_string(program)
        return self.run()

    def reset(self, loggers: Dict[str, Logger]):
        self.bubble_chamber.reset(loggers)
        self.coderack = Coderack.setup(self.bubble_chamber, loggers)
        loggers["structure"].coderack = self.coderack

    def run(self):
        for _ in range(self.NUMBER_OF_START_CHUNK_SUGGESTERS):
            self.coderack.add_codelet(ChunkSuggester.make("", self.bubble_chamber, 1.0))
        while self.bubble_chamber.result is None:
            try:
                if self.coderack.codelets_run % self.activation_update_frequency == 0:
                    if not HyperParameters.TESTING:
                        self.print_status_update()
                    self.bubble_chamber.update_activations()
                if self.coderack.codelets_run >= self.CODELET_RUN_LIMIT:
                    raise NoMoreCodelets
                self.coderack.select_and_run_codelet()
            except NoMoreCodelets:
                self.loggers["error"].log_message("No more codelets.")
                break
            except Exception as e:
                raise e
        self.print_results()
        return {
            "random_seed": self.bubble_chamber.random_machine.seed,
            "result": self.bubble_chamber.result,
            "worldview": self.bubble_chamber.worldview.view.structure_id
            if self.bubble_chamber.worldview.view is not None
            else "None",
            "satisfaction": self.bubble_chamber.worldview.satisfaction,
            "codelets_run": self.coderack.codelets_run,
        }

    def print_status_update(self):
        codelets_run = self.coderack.codelets_run
        bubble_chamber_satisfaction = self.bubble_chamber.satisfaction
        coderack_population = len(self.coderack._codelets)
        view_count = len(self.bubble_chamber.views)
        focus = (
            self.bubble_chamber.focus.view.structure_id
            + self.bubble_chamber.focus.view.parent_frame.name
            if self.bubble_chamber.focus.view is not None
            else None
        )
        focus_unhappiness = (
            self.bubble_chamber.focus.view.unhappiness
            if self.bubble_chamber.focus.view is not None
            else "-"
        )
        focus_satisfaction = (
            self.bubble_chamber.focus.satisfaction
            if self.bubble_chamber.focus.view is not None
            else "-"
        )
        print("=" * 200)
        print(
            f"codelets run: {codelets_run}; "
            + f"satisf.: {bubble_chamber_satisfaction}; "
            + f"determ.: {self.bubble_chamber.random_machine.determinism}; "
            + f"coderack pop.: {coderack_population}; "
            + f"view count.: {view_count}; "
            + f"recycle bin: {len(self.bubble_chamber.recycle_bin)}; "
            + f"Focus: {focus} (unhappy: {focus_unhappiness}; satisf.: {focus_satisfaction})"
        )
        if self.bubble_chamber.worldview.view is not None:
            view_output = self.bubble_chamber.worldview.output
            print(view_output)
        print("=" * 200)

    def print_results(self):
        print(
            f"Seed: {self.bubble_chamber.random_machine.seed} | "
            + f"Codelets run: {self.coderack.codelets_run} | "
            + f"Satisfaction: {self.bubble_chamber.worldview.satisfaction} |"
        )
        print(f"Result: {self.bubble_chamber.result}")
