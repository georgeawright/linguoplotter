import json
import os
import re

from matplotlib import pyplot


def generate_plot(log_directory, structures, field, title):
    figure = pyplot.figure()
    ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.set_title(title)

    for structure in structures:
        structure_directory = f"{log_directory}/structures/structures/{structure}"
        log_files = os.listdir(structure_directory)
        log_files.sort(key=lambda x: int(x.split(".")[0]))

        field_history_x = []
        field_history_y = []

        for log_file in log_files:
            time = int(log_file.split(".")[0])
            field_history_x.append(time)
            file_name = f"{structure_directory}/{log_file}"
            with open(file_name, "r") as f:
                file_data = json.load(f)
                field_history_y.append(file_data[field])
                label = file_data["name"] if "name" in file_data else structure

        print(field_history_x)
        print()
        print(field_history_y)

        (line,) = ax.plot(field_history_x, field_history_y)
        line.set_label(label)
        ax.legend()
        ax.set_xlabel("Codelets Run")
        ax.set_ylabel(field)

    file_name = title.replace(" ", "_")
    pyplot.savefig(f"{log_directory}/{file_name}.png")


concept_file_map = {
    # activities
    "suggest": None,
    "build": None,
    "evaluate": None,
    "select": None,
    "publish": None,
    # structures
    "correspondence": None,
    "chunk": None,
    "label": None,
    "letter-chunk": None,
    "relation": None,
    "view-simplex": None,
    # semantic
    "hot": None,
    "warm": None,
    "mild": None,
    "cool": None,
    "cold": None,
    "north": None,
    "south": None,
    "east": None,
    "west": None,
    "northwest": None,
    "northeast": None,
    "southwest": None,
    "southeast": None,
    "central": None,
    "everywhere": None,
}

log_directories = os.listdir("logs/")
log_directories.sort()
print(log_directories)
log_directory = "logs/" + log_directories[-1]

structures_directory = f"{log_directory}/structures/structures/"
log_files = os.listdir(structures_directory)
for log_file in log_files:
    if re.match(r"Concept[1-9]", log_file):
        file_name = f"{structures_directory}/{log_file}/0.json"
        try:
            with open(file_name, "r") as f:
                file_data = json.load(f)
                if file_data["name"] in concept_file_map:
                    concept_file_map[file_data["name"]] = log_file
        except FileNotFoundError:
            pass

print(concept_file_map)

generate_plot(
    log_directory,
    [
        concept_file_map["suggest"],
        concept_file_map["build"],
        concept_file_map["evaluate"],
        concept_file_map["select"],
        concept_file_map["publish"],
    ],
    "activation",
    "Activity Concepts Activation Over Time",
)

generate_plot(
    log_directory,
    [
        concept_file_map["correspondence"],
        concept_file_map["chunk"],
        concept_file_map["label"],
        concept_file_map["letter-chunk"],
        concept_file_map["relation"],
        concept_file_map["view-simplex"],
    ],
    "activation",
    "Structure Concepts Activation Over Time",
)

generate_plot(
    log_directory,
    [
        concept_file_map["hot"],
        concept_file_map["warm"],
        concept_file_map["mild"],
        concept_file_map["cool"],
        concept_file_map["cold"],
        concept_file_map["north"],
        concept_file_map["south"],
        concept_file_map["east"],
        concept_file_map["west"],
        concept_file_map["northwest"],
        concept_file_map["northeast"],
        concept_file_map["southwest"],
        concept_file_map["southeast"],
        concept_file_map["central"],
        concept_file_map["everywhere"],
    ],
    "activation",
    "Semantic Concepts Activation Over Time",
)