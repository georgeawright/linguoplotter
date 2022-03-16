import os
import time
from unittest.mock import Mock

from homer import Homer
from homer.loggers import ActivityLogger, StructureLogger

time_string = str(time.time())
logs_dir_path = f"logs/{time_string}"
os.mkdir(logs_dir_path)
structure_logs_dir_path = f"{logs_dir_path}/structures"
os.mkdir(structure_logs_dir_path)

activity_stream = open(f"{logs_dir_path}/activity.log", "w")
satisfaction_stream = open(f"{logs_dir_path}/satisfaction.csv", "w")
loggers = {
    "activity": ActivityLogger(activity_stream, satisfaction_stream),
    "structure": StructureLogger(f"{structure_logs_dir_path}"),
    "errors": Mock(),
}
narrator = Homer.setup(loggers, random_seed=1)

with open("program.lisp", "r") as f:
    program = f.read()
    narrator.run_program(program)

activity_stream.close()
