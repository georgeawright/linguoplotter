import math
from homer.logger import Logger


class StructureLogger(Logger):
    def __init__(self, directory: str):
        self.directory = directory if directory[-1] != "/" else directory[:-1]

    def log(self, structure):
        pass

    def log_concepts_and_frames(self, bubble_chamber, coderack):
        """output dot file of concepts, frames, connections, and activations"""
        codelets_run = coderack.codelets_run
        output_file_path = f"{self.directory}/concepts_and_frames/{codelets_run}.dot"
        with open(output_file_path, "w") as f:
            f.write("digraph G {\n")
            space_count = 0
            graphed_nodes = {}
            for space in bubble_chamber.conceptual_spaces.where(is_slot=False):
                nodes = space.contents.filter(
                    lambda x: not x.is_slot
                    and (x.is_concept or x.is_letter_chunk)
                    and x.parent_space == space
                )
                if nodes.is_empty():
                    continue
                f.write(f"subgraph cluster_{space_count} {{\n")
                f.write("style=filled; color=pink; node [style=filled, color=white];\n")
                for node in nodes:
                    node_name = (
                        node.name.upper() if node.is_concept else node.name.lower()
                    )
                    node_size = node.activation * 30 + 10
                    f.write(
                        f'{node.structure_id} [label="{node_name}" fontsize={node_size}];\n'
                    )
                    graphed_nodes[node] = True
                space_name = space.name.upper()
                f.write(f'label="{space_name}";\n')
                f.write("}\n")
                space_count += 1
            for node in graphed_nodes:
                for link in node.links_out.filter(
                    lambda x: x.start in graphed_nodes and x.end in graphed_nodes
                ):
                    start_id = link.start.structure_id
                    end_id = link.end.structure_id
                    label_name = (
                        link.parent_concept.name.upper()
                        if link.parent_concept is not None
                        else ""
                    )
                    color_number = math.ceil((1 - link.activation) * 200)
                    color_hex = hex(color_number)[2:]
                    if len(color_hex) == 1:
                        color_hex = "0" + color_hex
                    color_code = "#" + color_hex * 3
                    f.write(
                        f"{start_id} -> {end_id} "
                        + f'[label="{label_name}", color="{color_code}"];\n'
                    )
            f.write("}\n")

    def log_structure(self, structure):
        """output json file of structure attributes"""
