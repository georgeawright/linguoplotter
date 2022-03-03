from homer.codelet_result import CodeletResult
from homer.logger import Logger


class ActivityLogger(Logger):
    def __init__(self, stream, satisfaction_stream=None):
        self.stream = stream
        self.satisfaction_stream = satisfaction_stream
        self.previous_codelet_id = None
        self.codelets_run = 0
        self.LINE_WIDTH = 120

    def log(self, codelet: "Codelet", message: str):
        if codelet.codelet_id != self.previous_codelet_id:
            self.codelets_run += 1
            self._log_satisfaction(codelet)
            self.previous_codelet_id = codelet.codelet_id
            codelet_title = f" Codelet run {self.codelets_run}: {codelet.codelet_id} "
            no_of_dashes = (self.LINE_WIDTH - len(codelet_title)) // 2
            codelet_title = "-" * no_of_dashes + codelet_title + "-" * no_of_dashes
            if len(codelet_title) < self.LINE_WIDTH:
                codelet_title += "-"
            self.stream.write(f"\n{codelet_title}\n")
            self.stream.write(
                f"Parent: {codelet.parent_id} | Urgency: {codelet.urgency}\n"
            )
        self.stream.write(f"{message}\n")

    def _log_satisfaction(self, codelet: "Codelet"):
        if self.satisfaction_stream is not None:
            self.satisfaction_stream.write(
                f"{self.codelets_run},{codelet.bubble_chamber.satisfaction}\n"
            )

    def log_dict(self, codelet: "Codelet", dictionary, name: str):
        if dictionary is None or len(dictionary) == 0:
            self.log(codelet, "No " + name.lower())
        else:
            self.log(codelet, f"{name}: {{")
            for key, value in dictionary.items():
                self.log(codelet, f"    {key}: {value},")
            self.log(codelet, "}")

    def log_collection(self, codelet: "Codelet", collection, name: str):
        if collection is None or len(collection) == 0:
            self.log(codelet, "No " + name.lower())
        else:
            self.log(codelet, f"{name}: [")
            for item in collection:
                self.log(codelet, f"    {item},")
            self.log(codelet, "]")

    def log_result(self, codelet: "Codelet"):
        if CodeletResult.FINISH == codelet.result:
            self.log(codelet, "Result: FINISH")
        if CodeletResult.FIZZLE == codelet.result:
            self.log(codelet, "Result: FIZZLE")
        self.log(codelet, "-" * self.LINE_WIDTH)

    def log_targets_dict(self, codelet: "Codelet"):
        self.log_dict(codelet, codelet.targets_dict, "Target structures")

    def log_targets_collection(self, codelet: "Codelet"):
        self.log_collection(codelet, codelet.target_structures, "Target structures")

    def log_follow_ups(self, codelet: "Codelet"):
        self.log_collection(codelet, codelet.child_codelets, "Follow ups")

    def log_child_structures(self, codelet: "Codelet"):
        self.log_collection(codelet, codelet.child_structures, "Child structures")

    def log_champions(self, codelet: "Codelet"):
        self.log_collection(codelet, codelet.champions, "Champions")

    def log_challengers(self, codelet: "Codelet"):
        self.log_collection(codelet, codelet.challengers, "Challengers")

    def log_winners(self, codelet: "Codelet"):
        self.log_collection(codelet, codelet.winners, "Winners")

    def log_losers(self, codelet: "Codelet"):
        self.log_collection(codelet, codelet.challengers, "Losers")
