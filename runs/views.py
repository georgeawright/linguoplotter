import io
import re

from django.db.models import Q
from django.http import HttpResponse
from matplotlib import pyplot
import numpy

from .models import (
    CodeletRecord,
    CoderackRecord,
    StructureRecord,
    StructureUpdateRecord,
    RunRecord,
)


def index(request):
    runs = RunRecord.objects.order_by("-start_time")
    list_of_runs = "".join(
        [
            '<a href="' + str(run.id) + '"><li>' + str(run.start_time) + "</li></a>"
            for run in runs
        ]
    )
    output = "<ul>" + list_of_runs + "</ul>"
    return HttpResponse(output)


def run_view(request, run_id):
    def last_value_of_dict(dictionary):
        try:
            return dictionary[max(k for k in dictionary.keys())]
        except ValueError:
            return None

    coderack_record = CoderackRecord.objects.get(run_id=run_id)
    output = "<h1>Basic Run information:</h1>"
    output += "<ul>"
    output += "<li>Codelets Run: " + str(coderack_record.codelets_run[-1])
    output += "</ul>"
    output += '<p><a href="activity-and-structure-concepts">Activity and structure concepts</a></p>'
    output += '<p><a href="codelets">Codelets</a></p>'
    output += '<p><a href="structures">Structures</a></p>'
    output += f'<img src="/runs/{run_id}/coderack_population">'
    output += f'<img src="/runs/{run_id}/bubble_chamber_satisfaction">'
    structure_records = StructureRecord.objects.filter(run_id=run_id).all()
    last_column = 0
    last_row = 0
    original_chunks = []
    for record in structure_records:
        if not re.match("^Chunk", record.structure_id):
            continue
        if record.parent_codelet is not None:
            continue
        original_chunks.append(record)
        if record.location[0] > last_row:
            last_row = record.location[0]
        if record.location[1] > last_column:
            last_column = record.location[1]
    original_chunks_matrix = [
        [None for _ in range(last_column + 1)] for _ in range(last_row + 1)
    ]
    for original_chunk in original_chunks:
        row = original_chunk.location[0]
        column = original_chunk.location[1]
        original_chunks_matrix[row][column] = original_chunk
    output += "<h2>Raw Input</h2>"
    output += '<table border="1">'
    for i in range(last_row + 1):
        output += "<tr>"
        for j in range(last_column + 1):
            output += "<td>"
            output += str(original_chunks_matrix[i][j].value)
            output += "</td>"
        output += "</tr>"
    output += "</table>"
    output += "<h2>Labels</h2>"
    output += '<table border="1">'
    for i in range(last_row + 1):
        output += "<tr>"
        for j in range(last_column + 1):
            output += "<td>"
            original_chunk = original_chunks_matrix[i][j]
            output += "".join(
                [
                    f"{link.value} " + str(last_value_of_dict(link.quality)) + "<br>"
                    for link in original_chunk.links.all()
                    if re.match(r"^Label*", link.structure_id)
                ]
            )
            output += "</td>"
        output += "</tr>"
    output += "</table>"
    chunks = [
        structure
        for structure in structure_records
        if re.match("^Chunk*", structure.structure_id)
    ]
    output += "<h2>Chunks</h2>"
    for chunk in chunks:
        if chunk in original_chunks:
            continue
        output += f"<h3>{chunk.structure_id}</h3>"
        output += "".join(
            [
                f"{link.value} " + str(last_value_of_dict(link.quality)) + "<br>"
                for link in chunk.links.all()
                if re.match(r"^Label*", link.structure_id)
            ]
        )
        output += '<table border="1">'
        for i in range(last_row + 1):
            output += "<tr>"
            for j in range(last_column + 1):
                if original_chunks_matrix[i][j] in chunk.members.all():
                    output += '<td style="background-color: coral;">'
                else:
                    output += "<td>"
                output += str(original_chunks_matrix[i][j].value)
                output += "</td>"
            output += "</tr>"
        output += "</table>"
    relations = [
        structure
        for structure in structure_records
        if re.match(r"^Relation*", structure.structure_id)
    ]
    output += "<h2>Relations</h2>"
    for relation in relations:
        try:
            output += (
                f"{relation.structure_id}: "
                + f"{relation.value}("
                + f"{relation.parent_space.structure_id}, "
                + f"{relation.start.structure_id}, "
                + f"{relation.end.structure_id}) "
                + str(last_value_of_dict(relation.quality))
            )
            output += "<br>"
        except AttributeError:
            pass  # relations with no parent space are links between concepts
    return HttpResponse(output)


def coderack_population_view(request, run_id):
    coderack_record = CoderackRecord.objects.get(run_id=run_id)
    x = coderack_record.codelets_run
    y = coderack_record.population
    pyplot.clf()
    pyplot.title("Coderack Population")
    pyplot.xlabel("Codelets Run")
    pyplot.ylabel("Codelets on Rack")
    pyplot.plot(x, y)
    buf = io.BytesIO()
    pyplot.savefig(buf, format="svg", bbox_inches="tight")
    svg = buf.getvalue()
    buf.close()
    return HttpResponse(svg, content_type="image/svg+xml")


def bubble_chamber_satisfaction_view(request, run_id):
    coderack_record = CoderackRecord.objects.get(run_id=run_id)
    x = coderack_record.codelets_run
    y = coderack_record.satisfaction
    pyplot.clf()
    pyplot.title("Bubble Chamber Satisfaction")
    pyplot.xlabel("Codelets Run")
    pyplot.ylabel("Satisfaction")
    pyplot.plot(x, y)
    buf = io.BytesIO()
    pyplot.savefig(buf, format="svg", bbox_inches="tight")
    svg = buf.getvalue()
    buf.close()
    return HttpResponse(svg, content_type="image/svg+xml")


def activity_and_structure_concepts_view(request, run_id):
    build_record = StructureRecord.objects.get(
        run_id=run_id, structure_id__regex=r"^Concept*", value="build"
    )
    evaluate_record = StructureRecord.objects.get(
        run_id=run_id, structure_id__regex=r"^Concept*", value="evaluate"
    )
    select_record = StructureRecord.objects.get(
        run_id=run_id, structure_id__regex=r"^Concept*", value="select"
    )
    build_relations = (
        build_record.links.filter(~Q(end=evaluate_record))
        .filter(~Q(end=build_record))
        .all()
    )
    evaluate_relations = (
        evaluate_record.links.filter(~Q(end=select_record))
        .filter(~Q(end=evaluate_record))
        .all()
    )
    select_relations = (
        select_record.links.filter(~Q(end=build_record))
        .filter(~Q(end=select_record))
        .all()
    )

    pyplot.clf()
    figure, charts = pyplot.subplots(nrows=2, ncols=2, figsize=(15, 10))
    figure.suptitle("Activity and Structure Concept Activations")

    for concept_record in [build_record, evaluate_record, select_record]:
        data = [
            (int(codelets_run), activation)
            for codelets_run, activation in concept_record.activation.items()
        ]
        data.sort()
        x = [codelets_run for codelets_run, _ in data]
        y = [activation for _, activation in data]
        charts[0, 0].plot(x, y, label=concept_record.value)
    charts[0, 0].set_title("Activity Concept Activations")
    charts[0, 0].set(xlabel="Codelets Run", ylabel="Activation")
    charts[0, 0].legend(loc="best")

    for relation in build_relations:
        data = [
            (int(codelets_run), activation)
            for codelets_run, activation in relation.activation.items()
        ]
        data.sort()
        x = [codelets_run for codelets_run, _ in data]
        y = [activation for _, activation in data]
        charts[0, 1].plot(x, y, label=f"{relation.start.value}-{relation.end.value}")
    charts[0, 1].set_title("Activations of structure relations with build concept")
    charts[0, 1].set(xlabel="Codelets Run", ylabel="Activation")
    charts[0, 1].legend(loc="best")

    for relation in evaluate_relations:
        data = [
            (int(codelets_run), activation)
            for codelets_run, activation in relation.activation.items()
        ]
        data.sort()
        x = [codelets_run for codelets_run, _ in data]
        y = [activation for _, activation in data]
        charts[1, 0].plot(x, y, label=f"{relation.start.value}-{relation.end.value}")
    charts[1, 0].set_title("Activations of structure relations with evaluate concept")
    charts[1, 0].set(xlabel="Codelets Run", ylabel="Activation")
    charts[1, 0].legend(loc="best")

    for relation in select_relations:
        data = [
            (int(codelets_run), activation)
            for codelets_run, activation in relation.activation.items()
        ]
        data.sort()
        x = [codelets_run for codelets_run, _ in data]
        y = [activation for _, activation in data]
        charts[1, 1].plot(x, y, label=f"{relation.start.value}-{relation.end.value}")
    charts[1, 1].set_title("Activations of structure relations with select concept")
    charts[1, 1].set(xlabel="Codelets Run", ylabel="Activation")
    charts[1, 1].legend(loc="best")

    buf = io.BytesIO()
    figure.savefig(buf, format="svg", bbox_inches="tight")
    svg = buf.getvalue()
    buf.close()
    return HttpResponse(svg, content_type="image/svg+xml")


def codelets_view(request, run_id):
    codelet_records = (
        CodeletRecord.objects.filter(run_id=run_id)
        .filter(~Q(time_run=None))
        .order_by("time_run")
    )
    output = "<h1>Codelets in order run</h1>"
    output += "<ul>"
    output += "".join(
        [
            '<li><a href="'
            + codelet.codelet_id
            + '">'
            + codelet.codelet_id
            + "</a></li>"
            for codelet in codelet_records
        ]
    )
    output += "</ul>"
    return HttpResponse(output)


def codelet_view(request, run_id, codelet_id):
    codelet_record = CodeletRecord.objects.get(run_id=run_id, codelet_id=codelet_id)
    output = "<h1>" + codelet_id + "</h1>"
    output += "<ul>"
    output += "<li>Birth Time: " + str(codelet_record.birth_time) + "</li>"
    output += "<li>Time Run: " + str(codelet_record.time_run) + "</li>"
    output += "<li>Urgency: " + str(codelet_record.urgency) + "</li>"
    output += "<li>Target Structure: "
    if codelet_record.target_structure is not None:
        output += (
            '<a href="/runs/'
            + str(run_id)
            + "/structures/"
            + codelet_record.target_structure.structure_id
            + '/">'
            + codelet_record.target_structure.structure_id
            + "</a></li>"
        )
    else:
        output += "None</li>"
    output += "<li>Parent Codelet: "
    if codelet_record.parent is not None:
        output += (
            '<a href="/runs/'
            + str(run_id)
            + "/codelets/"
            + codelet_record.parent.codelet_id
            + '/">'
            + codelet_record.parent.codelet_id
            + "</a></li>"
        )
    else:
        output += "None</li>"
    output += "<li>Follow up: "
    try:
        follow_up = CodeletRecord.objects.get(run_id=run_id, parent=codelet_record)
        output += (
            '<a href="/runs/'
            + str(run_id)
            + "/codelets/"
            + follow_up.codelet_id
            + '/">'
            + follow_up.codelet_id
            + "</a></li>"
        )
    except CodeletRecord.DoesNotExist:
        output += "None</li>"
    output += "<li>Child Structure: "
    try:
        child_structure = StructureRecord.objects.get(
            run_id=run_id, parent_codelet=codelet_record.id
        )
        output += (
            '<a href="/runs/'
            + str(run_id)
            + "/structures/"
            + child_structure.structure_id
            + '/">'
            + child_structure.structure_id
            + "</a></li>"
        )
    except StructureRecord.DoesNotExist:
        output += "None</li>"
    output += "</ul>"
    return HttpResponse(output)


def structures_view(request, run_id):
    structure_records = StructureRecord.objects.filter(run_id=run_id).order_by(
        "structure_id"
    )
    output = "<h1>Structures</h1>"
    output += "<ul>"
    output += "".join(
        [
            '<li><a href="'
            + structure.structure_id
            + '">'
            + structure.structure_id
            + "</a></li>"
            for structure in structure_records
        ]
    )
    output += "</ul>"
    return HttpResponse(output)


def structure_view(request, run_id, structure_id):
    structure_record = StructureRecord.objects.get(
        run_id=run_id, structure_id=structure_id
    )
    output = "<h1>" + structure_id + "</h1>"
    output += "<ul>"
    output += "<li>Birth Time: " + str(structure_record.time_created) + "</li>"
    output += "<li>Value: " + structure_record.value + "</li>"
    output += "<li>Location: " + str(structure_record.location) + "</li>"
    if structure_record.parent_codelet is not None:
        output += (
            '<li>Parent Codelet: <a href="/runs/'
            + str(run_id)
            + "/codelets/"
            + structure_record.parent_codelet.codelet_id
            + '">'
            + structure_record.parent_codelet.codelet_id
            + "</a></li>"
        )
    else:
        output += "<li>Parent Codelet: None</li>"
    if structure_record.parent_concept is not None:
        output += (
            '<li>Parent Concept: <a href="/runs/'
            + str(run_id)
            + "/concepts/"
            + structure_record.parent_concept.structure_id
            + '">'
            + structure_record.parent_concept.structure_id
            + "</a></li>"
        )
    else:
        output += "<li>Parent Concept: None</li>"
    if structure_record.connections is None:
        output += "<li>Connections: None</li>"
    else:
        output += "<li>Connections: " + ", ".join(
            [
                '<a href="/runs/'
                + str(run_id)
                + "/structures/"
                + connection.structure_id
                + '">'
                + connection.structure_id
                + "</a>"
                for connection in structure_record.connections.all()
            ]
        )
        output += "</li>"
    output += "<li>Activation: " + str(structure_record.activation) + "</li>"
    output += "<li>Unhappiness : " + str(structure_record.unhappiness) + "</li>"
    output += "<li>Quality: " + str(structure_record.quality) + "</li>"
    output += "</ul>"
    if re.match(r"^Group*", structure_record.structure_id):
        structure_records = StructureRecord.objects.filter(run_id=run_id).all()
        last_column = 0
        last_row = 0
        raw_structures = []
        for record in structure_records:
            if not re.match("^RawStructure", record.structure_id):
                continue
            raw_structures.append(record)
            if record.location[1] > last_row:
                last_row = record.location[1]
            if record.location[2] > last_column:
                last_column = record.location[2]
        raw_structures_matrix = [
            [None for _ in range(last_column + 1)] for _ in range(last_row + 1)
        ]
        for raw_structure in raw_structures:
            row = raw_structure.location[1]
            column = raw_structure.location[2]
            raw_structures_matrix[row][column] = raw_structure
        output += '<table border="1">'
        for i in range(last_row + 1):
            output += "<tr>"
            for j in range(last_column + 1):
                if structure_record in raw_structures_matrix[i][j].connections.all():
                    output += '<td style="background-color: coral;">'
                else:
                    output += "<td>"
                output += str(raw_structures_matrix[i][j].value)
                output += "</td>"
            output += "</tr>"
        output += "</table>"
    output += "<h2>History</h2>"
    updates = StructureUpdateRecord.objects.filter(
        run_id=run_id, structure=structure_record
    ).order_by("time")
    for update in updates:
        output += (
            f"<p>{update.time}: {update.action} by "
            + f'<a href="/runs/{run_id}/codelets/{update.codelet.codelet_id}">'
            + f"{update.codelet.codelet_id}</a>.</p>"
        )
    return HttpResponse(output)
