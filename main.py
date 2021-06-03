import random
import statistics

from homer import Homer, StructureCollection
from homer.classifiers import (
    DifferenceClassifier,
    DifferentnessClassifier,
    SamenessClassifier,
    PartOfSpeechClassifier,
    ProximityClassifier,
    RuleClassifier,
)
from homer.id import ID
from homer.location import Location
from homer.locations import TwoPointLocation

random.seed(123)
from homer.loggers import DjangoLogger
from homer.structures.nodes import Chunk, Word
from homer.tools import centroid_euclidean_distance
from homer.word_form import WordForm


def setup_homer() -> Homer:
    problem = [
        [4, 5, 6, 4, 3],
        [10, 10, 7, 4, 4],
        [10, 11, 13, 16, 17],
        [10, 13, 16, 16, 19],
        [13, 20, 22, 19, 21],
        [22, 22, 24, 23, 22],
    ]

    path_to_logs = "logs"
    logger = DjangoLogger.setup(path_to_logs)
    homer = Homer.setup(logger)

    top_level_conceptual_space = homer.bubble_chamber.spaces["top level"]
    top_level_working_space = top_level_conceptual_space.instance_in_space(
        None, name="top level working"
    )

    input_concept = homer.def_concept(
        name="input",
        parent_space=top_level_conceptual_space,
        distance_function=centroid_euclidean_distance,
    )
    input_space = homer.def_working_space(
        name="input",
        parent_concept=input_concept,
        locations=[Location([], top_level_working_space)],
    )
    interpretation_concept = homer.def_concept(
        name="interpretation",
        parent_space=top_level_conceptual_space,
    )
    activity_concept = homer.def_concept(
        name="activity",
        parent_space=top_level_conceptual_space,
    )
    activities_space = homer.def_conceptual_space(
        name="activities",
        parent_concept=activity_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    suggest_concept = homer.def_concept(
        name="suggest",
        parent_space=activities_space,
        activation=1.0,
    )
    build_concept = homer.def_concept(
        name="build",
        parent_space=activities_space,
        activation=1.0,
    )
    evaluate_concept = homer.def_concept(
        name="evaluate",
        parent_space=activities_space,
    )
    select_concept = homer.def_concept(
        name="select",
        parent_space=activities_space,
    )
    publish_concept = homer.def_concept(
        name="publish",
        parent_space=activities_space,
    )
    space_type_concept = homer.def_concept(
        name="space type",
        parent_space=top_level_conceptual_space,
    )
    space_types_space = homer.def_conceptual_space(
        name="space types",
        parent_concept=space_type_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    inner_concept = homer.def_concept(
        name="inner",
        parent_space=space_types_space,
    )
    outer_concept = homer.def_concept(
        name="outer",
        parent_space=space_types_space,
    )
    direction_concept = homer.def_concept(
        name="direction",
        parent_space=top_level_conceptual_space,
    )
    directions_space = homer.def_conceptual_space(
        name="directions",
        parent_concept=direction_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    forward_concept = homer.def_concept(
        name="forward",
        parent_space=directions_space,
    )
    reverse_concept = homer.def_concept(
        name="reverse",
        parent_space=directions_space,
    )
    structure_concept = homer.def_concept(
        name="structure",
        parent_space=top_level_conceptual_space,
    )
    structures_space = homer.def_conceptual_space(
        name="structures",
        parent_concept=structure_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    chunk_concept = homer.def_concept(
        name="chunk",
        parent_space=structures_space,
    )
    view_concept = homer.def_concept(
        name="view",
        parent_space=structures_space,
    )
    view_discourse_concept = homer.def_concept(
        name="view-discourse",
        parent_space=structures_space,
    )
    view_monitoring_concept = homer.def_concept(
        name="view-monitoring",
        parent_space=structures_space,
    )
    view_simplex_concept = homer.def_concept(
        name="view-simplex",
        parent_space=structures_space,
    )
    word_concept = homer.def_concept(
        name="word",
        parent_space=structures_space,
        instance_type=str,
    )
    phrase_concept = homer.def_concept(
        name="phrase",
        parent_space=structures_space,
    )
    label_concept = homer.def_concept(
        name="label",
        parent_space=structures_space,
    )
    relation_concept = homer.def_concept(
        name="relation",
        parent_space=structures_space,
    )
    correspondence_concept = homer.def_concept(
        name="correspondence",
        parent_space=structures_space,
    )
    template_concept = homer.def_concept(
        name="template",
        parent_space=structures_space,
    )
    text_concept = homer.def_concept(
        name="text",
        parent_space=structures_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    discourse_concept = homer.def_concept(
        name="discourse",
        parent_space=structures_space,
        instance_type=Word,
    )
    label_concepts_space = homer.def_conceptual_space(
        name="label concepts",
        parent_concept=label_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    relational_concepts_space = homer.def_conceptual_space(
        name="relational concepts",
        parent_concept=relation_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    correspondential_concepts_space = homer.def_conceptual_space(
        name="correspondential concepts",
        parent_concept=correspondence_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    templates_space = homer.def_conceptual_space(
        name="templates",
        parent_concept=template_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    text_space = homer.def_conceptual_space(
        name="text",
        parent_concept=text_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    # structure links
    homer.def_concept_link(inner_concept, chunk_concept, activation=1.0)
    homer.def_concept_link(chunk_concept, inner_concept, activation=1.0)
    homer.def_concept_link(chunk_concept, label_concept, activation=1.0)
    homer.def_concept_link(chunk_concept, relation_concept, activation=1.0)
    homer.def_concept_link(chunk_concept, view_concept, activation=1.0)
    homer.def_concept_link(label_concept, inner_concept, activation=1.0)
    homer.def_concept_link(relation_concept, inner_concept, activation=1.0)
    homer.def_concept_link(view_concept, view_discourse_concept, activation=1.0)
    homer.def_concept_link(view_concept, view_monitoring_concept, activation=1.0)
    homer.def_concept_link(view_concept, view_simplex_concept, activation=1.0)
    homer.def_concept_link(view_monitoring_concept, reverse_concept, activation=1.0)
    homer.def_concept_link(view_monitoring_concept, outer_concept, activation=1.0)
    homer.def_concept_link(reverse_concept, chunk_concept, activation=1.0)
    homer.def_concept_link(
        view_discourse_concept, correspondence_concept, activation=1.0
    )
    homer.def_concept_link(view_discourse_concept, word_concept, activation=1.0)
    homer.def_concept_link(view_simplex_concept, correspondence_concept, activation=1.0)
    homer.def_concept_link(view_simplex_concept, word_concept, activation=1.0)
    homer.def_concept_link(word_concept, phrase_concept, activation=1.0)
    homer.def_concept_link(word_concept, view_monitoring_concept, activation=1.0)
    homer.def_concept_link(word_concept, label_concept, activation=1.0)
    homer.def_concept_link(word_concept, relation_concept, activation=1.0)
    homer.def_concept_link(view_monitoring_concept, publish_concept, activation=1.0)

    # activity links
    homer.def_concept_link(suggest_concept, build_concept, activation=1.0)
    homer.def_concept_link(build_concept, evaluate_concept, activation=1.0)
    homer.def_concept_link(evaluate_concept, select_concept, activation=1.0)
    homer.def_concept_link(select_concept, suggest_concept, activation=1.0)

    # activity-structure links
    homer.def_concept_link(suggest_concept, correspondence_concept)
    homer.def_concept_link(suggest_concept, chunk_concept)
    homer.def_concept_link(suggest_concept, label_concept, activation=1.0)
    homer.def_concept_link(suggest_concept, phrase_concept)
    homer.def_concept_link(suggest_concept, relation_concept)
    homer.def_concept_link(suggest_concept, view_discourse_concept)
    homer.def_concept_link(suggest_concept, view_monitoring_concept)
    homer.def_concept_link(suggest_concept, view_simplex_concept)
    homer.def_concept_link(suggest_concept, word_concept)
    homer.def_concept_link(build_concept, correspondence_concept)
    homer.def_concept_link(build_concept, chunk_concept)
    homer.def_concept_link(build_concept, label_concept, activation=1.0)
    homer.def_concept_link(build_concept, phrase_concept)
    homer.def_concept_link(build_concept, relation_concept)
    homer.def_concept_link(build_concept, view_discourse_concept)
    homer.def_concept_link(build_concept, view_monitoring_concept)
    homer.def_concept_link(build_concept, view_simplex_concept)
    homer.def_concept_link(build_concept, word_concept)
    homer.def_concept_link(evaluate_concept, correspondence_concept)
    homer.def_concept_link(evaluate_concept, chunk_concept)
    homer.def_concept_link(evaluate_concept, label_concept)
    homer.def_concept_link(evaluate_concept, phrase_concept)
    homer.def_concept_link(evaluate_concept, relation_concept)
    homer.def_concept_link(evaluate_concept, view_discourse_concept)
    homer.def_concept_link(evaluate_concept, view_monitoring_concept)
    homer.def_concept_link(evaluate_concept, view_simplex_concept)
    homer.def_concept_link(evaluate_concept, word_concept)
    homer.def_concept_link(select_concept, correspondence_concept)
    homer.def_concept_link(select_concept, chunk_concept)
    homer.def_concept_link(select_concept, label_concept)
    homer.def_concept_link(select_concept, phrase_concept)
    homer.def_concept_link(select_concept, relation_concept)
    homer.def_concept_link(select_concept, view_discourse_concept)
    homer.def_concept_link(select_concept, view_monitoring_concept)
    homer.def_concept_link(select_concept, view_simplex_concept)
    homer.def_concept_link(select_concept, word_concept)

    # Grammatical Knowledge

    grammar_vectors = {
        "sentence": [],
        "np": [],
        "vp": [],
        "ap": [],
        "pp": [],
        "noun": [],
        "verb": [],
        "adj": [],
        "jjr": [],
        "adv": [],
        "cop": [],
        "prep": [],
        "det": [],
        "conj": [],
        "null": [],
    }
    for index, concept in enumerate(grammar_vectors):
        grammar_vectors[concept] = [0 for _ in grammar_vectors]
        grammar_vectors[concept][index] = 1

    dependency_vectors = {
        "det_r": [],
        "nsubj": [],
        "cop_r": [],
        "prep_r": [],
        "pobj": [],
        "dep": [],
    }
    for index, concept in enumerate(dependency_vectors):
        dependency_vectors[concept] = [0 for _ in dependency_vectors]
        dependency_vectors[concept][index] = 1

    grammar_concept = homer.def_concept(
        name="grammar",
        parent_space=label_concepts_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    grammatical_concepts_space = homer.def_conceptual_space(
        name="grammar",
        parent_concept=grammar_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        is_basic_level=True,
        is_symbolic=True,
    )
    sentence_concept = homer.def_concept(
        name="s",
        locations=[Location([grammar_vectors["sentence"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    np_concept = homer.def_concept(
        name="np",
        locations=[Location([grammar_vectors["np"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    vp_concept = homer.def_concept(
        name="vp",
        locations=[Location([grammar_vectors["vp"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    ap_concept = homer.def_concept(
        name="ap",
        locations=[Location([grammar_vectors["ap"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    pp_concept = homer.def_concept(
        name="pp",
        locations=[Location([grammar_vectors["pp"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    noun_concept = homer.def_concept(
        name="noun",
        locations=[Location([grammar_vectors["noun"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=PartOfSpeechClassifier(),
        distance_function=centroid_euclidean_distance,
    )
    verb_concept = homer.def_concept(
        name="verb",
        locations=[Location([grammar_vectors["verb"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=PartOfSpeechClassifier(),
        distance_function=centroid_euclidean_distance,
    )
    adj_concept = homer.def_concept(
        name="adj",
        locations=[Location([grammar_vectors["adj"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=PartOfSpeechClassifier(),
        distance_function=centroid_euclidean_distance,
    )
    jjr_concept = homer.def_concept(
        name="jjr",
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=PartOfSpeechClassifier(),
        distance_function=centroid_euclidean_distance,
    )
    adv_concept = homer.def_concept(
        name="adv",
        locations=[Location([grammar_vectors["adv"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=PartOfSpeechClassifier(),
        distance_function=centroid_euclidean_distance,
    )
    cop_concept = homer.def_concept(
        name="cop",
        locations=[Location([grammar_vectors["cop"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=PartOfSpeechClassifier(),
        distance_function=centroid_euclidean_distance,
    )
    prep_concept = homer.def_concept(
        name="prep",
        locations=[Location([grammar_vectors["prep"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=PartOfSpeechClassifier(),
        distance_function=centroid_euclidean_distance,
    )
    det_concept = homer.def_concept(
        name="det",
        locations=[Location([grammar_vectors["det"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=PartOfSpeechClassifier(),
        distance_function=centroid_euclidean_distance,
    )
    conj_concept = homer.def_concept(
        name="conj",
        locations=[Location([grammar_vectors["conj"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=PartOfSpeechClassifier(),
        distance_function=centroid_euclidean_distance,
    )
    null_concept = homer.def_concept(
        name="null",
        locations=[Location([grammar_vectors["null"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    s_np_vp = homer.def_rule(
        name="s --> np, vp",
        location=Location([], grammatical_concepts_space),
        root=sentence_concept,
        left_branch=np_concept,
        right_branch=vp_concept,
        stable_activation=1.0,
    )
    s_noun_vp = homer.def_rule(
        name="s --> noun, vp",
        location=Location([], grammatical_concepts_space),
        root=sentence_concept,
        left_branch=noun_concept,
        right_branch=vp_concept,
        stable_activation=1.0,
    )
    s_s_pp = homer.def_rule(
        name="s --> s, pp",
        location=Location([], grammatical_concepts_space),
        root=sentence_concept,
        left_branch=sentence_concept,
        right_branch=pp_concept,
        stable_activation=1.0,
    )
    # TODO: add S --> S conj S
    np_det_noun = homer.def_rule(
        name="np --> det, noun",
        location=Location([], grammatical_concepts_space),
        root=np_concept,
        left_branch=det_concept,
        right_branch=noun_concept,
        stable_activation=1.0,
    )
    vp_cop_adj = homer.def_rule(
        name="vp --> cop, adj",
        location=Location([], grammatical_concepts_space),
        root=vp_concept,
        left_branch=cop_concept,
        right_branch=adj_concept,
        stable_activation=1.0,
    )
    vp_cop_ap = homer.def_rule(
        name="vp --> cop, ap",
        location=Location([], grammatical_concepts_space),
        root=vp_concept,
        left_branch=cop_concept,
        right_branch=ap_concept,
        stable_activation=1.0,
    )
    vp_verb = homer.def_rule(
        name="vp --> verb",
        location=Location([], grammatical_concepts_space),
        root=vp_concept,
        left_branch=verb_concept,
        right_branch=null_concept,
        stable_activation=1.0,
    )
    ap_adj = homer.def_rule(
        name="ap --> adj",
        location=Location([], grammatical_concepts_space),
        root=ap_concept,
        left_branch=adj_concept,
        right_branch=null_concept,
        stable_activation=1.0,
    )
    pp_prep_np = homer.def_rule(
        name="pp --> prep, np",
        location=Location([], grammatical_concepts_space),
        root=pp_concept,
        left_branch=prep_concept,
        right_branch=np_concept,
        stable_activation=1.0,
    )
    dependency_concept = homer.def_concept(
        name="dependency",
        parent_space=relational_concepts_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    dependency_concepts_space = homer.def_conceptual_space(
        name="dependency",
        parent_concept=dependency_concept,
        locations=[Location([], relational_concepts_space)],
        no_of_dimensions=1,
        is_basic_level=True,
        is_symbolic=True,
    )
    det_r_concept = homer.def_concept(
        name="det_r",
        locations=[
            TwoPointLocation(
                [grammar_vectors["noun"]],
                [grammar_vectors["det"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["det_r"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=RuleClassifier(
            [
                lambda kwargs: kwargs["start"].location.coordinates[0][0]
                == kwargs["end"].location.coordinates[0][0] + 1,
                lambda kwargs: kwargs["start"].has_label(noun_concept),
                lambda kwargs: kwargs["end"].has_label(det_concept),
            ]
        ),
        distance_function=centroid_euclidean_distance,
    )
    nsubj_concept = homer.def_concept(
        name="nsubj",
        locations=[
            TwoPointLocation(
                [grammar_vectors["verb"]],
                [grammar_vectors["noun"]],
                grammatical_concepts_space,
            ),
            TwoPointLocation(
                [grammar_vectors["adj"]],
                [grammar_vectors["noun"]],
                grammatical_concepts_space,
            ),
            TwoPointLocation(
                [grammar_vectors["jjr"]],
                [grammar_vectors["noun"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["nsubj"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=RuleClassifier(
            [
                lambda kwargs: kwargs["end"].has_label(noun_concept),
                lambda kwargs: kwargs["start"].has_label(verb_concept)
                or (
                    (
                        kwargs["start"].has_label(adj_concept)
                        or kwargs["start"].has_label(jjr_concept)
                    )
                    and kwargs["start"].has_relation_with_name("cop_r")
                ),
                lambda kwargs: kwargs["end"].location.coordinates[0][0]
                < kwargs["start"].location.coordinates[0][0],
            ]
        ),
        distance_function=centroid_euclidean_distance,
    )
    cop_r_concept = homer.def_concept(
        name="cop_r",
        locations=[
            TwoPointLocation(
                [grammar_vectors["adj"]],
                [grammar_vectors["cop"]],
                grammatical_concepts_space,
            ),
            TwoPointLocation(
                [grammar_vectors["jjr"]],
                [grammar_vectors["cop"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["cop_r"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=RuleClassifier(
            [
                lambda kwargs: kwargs["end"].has_label(cop_concept),
                lambda kwargs: kwargs["start"].has_label(adj_concept)
                or kwargs["start"].has_label(jjr_concept),
                lambda kwargs: kwargs["start"].location.coordinates[0][0]
                == kwargs["end"].location.coordinates[0][0] + 1,
            ]
        ),
        distance_function=centroid_euclidean_distance,
    )
    prep_r_concept = homer.def_concept(
        name="prep_r",
        locations=[
            TwoPointLocation(
                [grammar_vectors["verb"]],
                [grammar_vectors["prep"]],
                grammatical_concepts_space,
            ),
            TwoPointLocation(
                [grammar_vectors["adj"]],
                [grammar_vectors["prep"]],
                grammatical_concepts_space,
            ),
            TwoPointLocation(
                [grammar_vectors["jjr"]],
                [grammar_vectors["prep"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["prep_r"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=RuleClassifier(
            [
                lambda kwargs: kwargs["end"].has_label(prep_concept),
                lambda kwargs: kwargs["start"].has_label(verb_concept)
                or (
                    (
                        kwargs["start"].has_label(adj_concept)
                        or kwargs["start"].has_label(jjr_concept)
                    )
                    and kwargs["start"].has_relation_with_name("cop_r")
                ),
                lambda kwargs: kwargs["start"].location.coordinates[0][0]
                < kwargs["end"].location.coordinates[0][0],
            ]
        ),
        distance_function=centroid_euclidean_distance,
    )
    pobj_concept = homer.def_concept(
        name="pobj",
        locations=[
            TwoPointLocation(
                [grammar_vectors["prep"]],
                [grammar_vectors["noun"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["pobj"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=RuleClassifier(
            [
                lambda kwargs: kwargs["end"].has_label(noun_concept),
                lambda kwargs: kwargs["start"].has_label(prep_concept),
                lambda kwargs: kwargs["start"].location.coordinates[0][0]
                < kwargs["end"].location.coordinates[0][0],
            ]
        ),
        distance_function=centroid_euclidean_distance,
    )
    dep_concept = homer.def_concept(
        name="dep",
        locations=[
            TwoPointLocation(
                [grammar_vectors["prep"]],
                [grammar_vectors["noun"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["dep"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        classifier=RuleClassifier(
            [
                lambda kwargs: kwargs["end"].has_label(noun_concept),
                lambda kwargs: kwargs["start"].has_label(prep_concept),
                lambda kwargs: kwargs["start"].has_relation_with_name("prep_r"),
                lambda kwargs: kwargs["start"]
                .relation_with_name("prep_r")
                .start.has_relation_with_name("pobj"),
                lambda kwargs: kwargs["end"].location.coordinates[0][0]
                > kwargs["start"].location.coordinates[0][0],
            ]
        ),
        distance_function=centroid_euclidean_distance,
    )

    homer.def_concept_link(det_concept, det_r_concept, activation=1.0)
    homer.def_concept_link(noun_concept, nsubj_concept, activation=1.0)
    homer.def_concept_link(noun_concept, pobj_concept, activation=1.0)
    homer.def_concept_link(noun_concept, dep_concept, activation=1.0)
    homer.def_concept_link(prep_concept, prep_r_concept, activation=1.0)
    homer.def_concept_link(prep_concept, pobj_concept, activation=1.0)
    homer.def_concept_link(prep_concept, dep_concept, activation=1.0)
    homer.def_concept_link(cop_concept, cop_r_concept, activation=1.0)
    homer.def_concept_link(cop_concept, nsubj_concept, activation=1.0)
    homer.def_concept_link(cop_concept, prep_r_concept, activation=1.0)
    homer.def_concept_link(verb_concept, nsubj_concept, activation=1.0)
    homer.def_concept_link(verb_concept, prep_r_concept, activation=1.0)
    homer.def_concept_link(adj_concept, nsubj_concept, activation=1.0)
    homer.def_concept_link(adj_concept, cop_r_concept, activation=1.0)
    homer.def_concept_link(adj_concept, prep_r_concept, activation=1.0)
    homer.def_concept_link(jjr_concept, nsubj_concept, activation=1.0)
    homer.def_concept_link(jjr_concept, cop_r_concept, activation=1.0)
    homer.def_concept_link(jjr_concept, prep_r_concept, activation=1.0)

    # Domain Specific Knowledge

    #    more_less_concept = homer.def_concept(
    #        name="more-less",
    #        parent_space=relational_concepts_space,
    #        distance_function=centroid_euclidean_distance,
    #    )
    #    more_less_space = homer.def_conceptual_space(
    #        name="more-less",
    #        locations=[Location([], relational_concepts_space)],
    #        parent_concept=more_less_concept,
    #        is_basic_level=True,
    #    )
    #    more = homer.def_concept(
    #        name="more",
    #        locations=[Location([[4]], more_less_space)],
    #        classifier=DifferenceClassifier(ProximityClassifier()),
    #        parent_space=more_less_space,
    #        distance_function=centroid_euclidean_distance,
    #    )
    #    more_lexeme = homer.def_lexeme(
    #        headword="more",
    #        forms={
    #            WordForm.HEADWORD: "more",
    #            WordForm.COMPARATIVE: "more",
    #            WordForm.SUPERLATIVE: "most",
    #        },
    #        parts_of_speech={
    #            WordForm.HEADWORD: [adv_concept],
    #            WordForm.COMPARATIVE: [adv_concept],
    #            WordForm.SUPERLATIVE: [adv_concept],
    #        },
    #        parent_concept=more,
    #    )
    #    homer.def_concept_link(adv_concept, more_lexeme)
    #    less = homer.def_concept(
    #        name="less",
    #        locations=[Location([[-4]], more_less_space)],
    #        classifier=DifferenceClassifier(ProximityClassifier()),
    #        parent_space=more_less_space,
    #        distance_function=centroid_euclidean_distance,
    #    )
    #    less_lexeme = homer.def_lexeme(
    #        headword="less",
    #        forms={
    #            WordForm.HEADWORD: "less",
    #            WordForm.COMPARATIVE: "less",
    #            WordForm.SUPERLATIVE: "least",
    #        },
    #        parts_of_speech={
    #            WordForm.HEADWORD: [adv_concept],
    #            WordForm.COMPARATIVE: [adv_concept],
    #            WordForm.SUPERLATIVE: [adv_concept],
    #        },
    #        parent_concept=less,
    #    )
    #    homer.def_concept_link(adv_concept, less_lexeme)
    same_different_concept = homer.def_concept(
        name="same-different",
        parent_space=correspondential_concepts_space,
        distance_function=centroid_euclidean_distance,
    )
    same_different_space = homer.def_conceptual_space(
        name="same-different",
        locations=[Location([], correspondential_concepts_space)],
        parent_concept=same_different_concept,
        is_basic_level=True,
    )
    same = homer.def_concept(
        name="same",
        classifier=SamenessClassifier(),
        parent_space=same_different_space,
        distance_function=centroid_euclidean_distance,
    )
    different = homer.def_concept(
        name="different",
        classifier=DifferentnessClassifier(),
        parent_space=same_different_space,
        distance_function=centroid_euclidean_distance,
    )
    temperature_concept = homer.def_concept(
        name="temperature",
        parent_space=label_concepts_space,
        distance_function=centroid_euclidean_distance,
    )
    temperature_space = homer.def_conceptual_space(
        name="temperature",
        parent_concept=temperature_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        is_basic_level=True,
    )
    hot = homer.def_concept(
        name="hot",
        locations=[Location([[22]], temperature_space)],
        classifier=ProximityClassifier(),
        parent_space=temperature_space,
        distance_function=centroid_euclidean_distance,
    )
    # homer.def_concept_link(hot, more)
    hot_lexeme = homer.def_lexeme(
        headword="hot",
        forms={
            WordForm.HEADWORD: "hot",
            WordForm.COMPARATIVE: "hotter",
            WordForm.SUPERLATIVE: "hottest",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=hot,
    )
    # homer.def_concept_link(adj_concept, hot_lexeme)
    warm = homer.def_concept(
        name="warm",
        locations=[Location([[16]], temperature_space)],
        classifier=ProximityClassifier(),
        parent_space=temperature_space,
        distance_function=centroid_euclidean_distance,
    )
    # homer.def_concept_link(warm, more)
    warm_lexeme = homer.def_lexeme(
        headword="warm",
        forms={
            WordForm.HEADWORD: "warm",
            WordForm.COMPARATIVE: "warmer",
            WordForm.SUPERLATIVE: "warmest",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=warm,
    )
    # homer.def_concept_link(adj_concept, warm_lexeme)
    mild = homer.def_concept(
        name="mild",
        locations=[Location([[10]], temperature_space)],
        classifier=ProximityClassifier(),
        parent_space=temperature_space,
        distance_function=centroid_euclidean_distance,
    )
    # homer.def_concept_link(mild, less)
    mild_lexeme = homer.def_lexeme(
        headword="mild",
        forms={
            WordForm.HEADWORD: "mild",
            WordForm.COMPARATIVE: "milder",
            WordForm.SUPERLATIVE: "mildest",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=mild,
    )
    # homer.def_concept_link(adj_concept, mild_lexeme)
    cold = homer.def_concept(
        name="cold",
        locations=[Location([[4]], temperature_space)],
        classifier=ProximityClassifier(),
        parent_space=temperature_space,
        distance_function=centroid_euclidean_distance,
    )
    # homer.def_concept_link(cold, less)
    cold_lexeme = homer.def_lexeme(
        headword="cold",
        forms={
            WordForm.HEADWORD: "cold",
            WordForm.COMPARATIVE: "colder",
            WordForm.SUPERLATIVE: "coldest",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=cold,
    )
    homer.def_concept_link(adj_concept, cold_lexeme)
    # hotter = homer.def_concept(
    #    name="more",
    #    locations=[TwoPointLocation([[None]], [[None]], temperature_space)],
    #    classifier=DifferenceClassifier(ProximityClassifier()),
    #    parent_space=temperature_space,
    #    distance_function=lambda x, y: True,
    # )
    # hotter_lexeme = homer.def_lexeme(
    #    headword="hotter",
    #    forms={
    #        WordForm.HEADWORD: "hotter",
    #    },
    #    parts_of_speech={
    #        WordForm.HEADWORD: [jjr_concept],
    #    },
    #    parent_concept=hotter,
    # )
    # homer.def_concept_link(jjr_concept, hotter_lexeme)
    # colder = homer.def_concept(
    #    name="colder",
    #    locations=[TwoPointLocation([[None]], [[None]], temperature_space)],
    #    classifier=DifferenceClassifier(ProximityClassifier()),
    #    parent_space=temperature_space,
    #    distance_function=lambda x, y: True,
    # )
    # colder_lexeme = homer.def_lexeme(
    #    headword="colder",
    #    forms={
    #        WordForm.HEADWORD: "colder",
    #    },
    #    parts_of_speech={
    #        WordForm.HEADWORD: [jjr_concept],
    #    },
    #    parent_concept=colder,
    # )
    # homer.def_concept_link(jjr_concept, colder_lexeme)
    location_concept = homer.def_concept(
        name="location",
        parent_space=label_concepts_space,
        distance_function=centroid_euclidean_distance,
    )
    north_south_space = homer.def_conceptual_space(
        name="north-south",
        parent_concept=location_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [[c[0]] for c in location.coordinates]
        },
    )
    west_east_space = homer.def_conceptual_space(
        name="west-east",
        parent_concept=location_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [[c[1]] for c in location.coordinates]
        },
    )
    nw_se_space = homer.def_conceptual_space(
        name="nw-se",
        parent_concept=location_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [
                [statistics.fmean(c)] for c in location.coordinates
            ]
        },
    )
    ne_sw_space = homer.def_conceptual_space(
        name="ne-sw",
        parent_concept=location_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [
                [statistics.fmean([c[0], 4 - c[1]])] for c in location.coordinates
            ]
        },
    )
    location_space = homer.def_conceptual_space(
        name="location",
        parent_concept=location_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=2,
        dimensions=[north_south_space, west_east_space],
        sub_spaces=[north_south_space, west_east_space, nw_se_space, ne_sw_space],
        is_basic_level=True,
    )
    north = homer.def_concept(
        name="north",
        locations=[Location([[0, 2]], location_space)],
        classifier=ProximityClassifier(),
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    north_lexeme = homer.def_lexeme(
        headword="north",
        forms={
            WordForm.HEADWORD: "north",
            WordForm.COMPARATIVE: "further north",
            WordForm.SUPERLATIVE: "furthest north",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept, noun_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=north,
    )
    homer.def_concept_link(adj_concept, north_lexeme)
    homer.def_concept_link(noun_concept, north_lexeme)
    homer.def_concept_link(nsubj_concept, north_lexeme)
    homer.def_concept_link(pobj_concept, north_lexeme)
    south = homer.def_concept(
        name="south",
        locations=[Location([[5, 2]], location_space)],
        classifier=ProximityClassifier(),
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    south_lexeme = homer.def_lexeme(
        headword="south",
        forms={
            WordForm.HEADWORD: "south",
            WordForm.COMPARATIVE: "further south",
            WordForm.SUPERLATIVE: "furthest south",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept, noun_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=south,
    )
    homer.def_concept_link(adj_concept, south_lexeme)
    homer.def_concept_link(noun_concept, south_lexeme)
    homer.def_concept_link(nsubj_concept, south_lexeme)
    homer.def_concept_link(pobj_concept, south_lexeme)
    east = homer.def_concept(
        name="east",
        locations=[Location([[2.5, 4]], location_space)],
        classifier=ProximityClassifier(),
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    east_lexeme = homer.def_lexeme(
        headword="east",
        forms={
            WordForm.HEADWORD: "east",
            WordForm.COMPARATIVE: "further east",
            WordForm.SUPERLATIVE: "furthest east",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept, noun_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=east,
    )
    homer.def_concept_link(adj_concept, east_lexeme)
    homer.def_concept_link(noun_concept, east_lexeme)
    homer.def_concept_link(nsubj_concept, east_lexeme)
    homer.def_concept_link(pobj_concept, east_lexeme)
    west = homer.def_concept(
        name="west",
        locations=[Location([[2.5, 0]], location_space)],
        classifier=ProximityClassifier(),
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    west_lexeme = homer.def_lexeme(
        headword="west",
        forms={
            WordForm.HEADWORD: "west",
            WordForm.COMPARATIVE: "further west",
            WordForm.SUPERLATIVE: "furthest west",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept, noun_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=west,
    )
    homer.def_concept_link(adj_concept, west_lexeme)
    homer.def_concept_link(noun_concept, west_lexeme)
    homer.def_concept_link(nsubj_concept, west_lexeme)
    homer.def_concept_link(pobj_concept, west_lexeme)
    northwest = homer.def_concept(
        name="northwest",
        locations=[Location([[0, 0]], location_space)],
        classifier=ProximityClassifier(),
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    northwest_lexeme = homer.def_lexeme(
        headword="northwest",
        forms={
            WordForm.HEADWORD: "northwest",
            WordForm.COMPARATIVE: "further northwest",
            WordForm.SUPERLATIVE: "furthest northwest",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept, noun_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=northwest,
    )
    homer.def_concept_link(adj_concept, northwest_lexeme)
    homer.def_concept_link(noun_concept, northwest_lexeme)
    homer.def_concept_link(nsubj_concept, northwest_lexeme)
    homer.def_concept_link(pobj_concept, northwest_lexeme)
    northeast = homer.def_concept(
        name="northeast",
        locations=[Location([[0, 4]], location_space)],
        classifier=ProximityClassifier(),
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    northeast_lexeme = homer.def_lexeme(
        headword="northeast",
        forms={
            WordForm.HEADWORD: "northeast",
            WordForm.COMPARATIVE: "further northeast",
            WordForm.SUPERLATIVE: "furthest northeast",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept, noun_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=northeast,
    )
    homer.def_concept_link(adj_concept, northeast_lexeme)
    homer.def_concept_link(noun_concept, northeast_lexeme)
    homer.def_concept_link(nsubj_concept, northeast_lexeme)
    homer.def_concept_link(pobj_concept, northeast_lexeme)
    southwest = homer.def_concept(
        name="southwest",
        locations=[Location([[5, 0]], location_space)],
        classifier=ProximityClassifier(),
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    southwest_lexeme = homer.def_lexeme(
        headword="southwest",
        forms={
            WordForm.HEADWORD: "southwest",
            WordForm.COMPARATIVE: "further southwest",
            WordForm.SUPERLATIVE: "furthest southwest",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept, noun_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=southwest,
    )
    homer.def_concept_link(adj_concept, southwest_lexeme)
    homer.def_concept_link(noun_concept, southwest_lexeme)
    homer.def_concept_link(nsubj_concept, southwest_lexeme)
    homer.def_concept_link(pobj_concept, southwest_lexeme)
    southeast = homer.def_concept(
        name="southeast",
        locations=[Location([[5, 4]], location_space)],
        classifier=ProximityClassifier(),
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    southeast_lexeme = homer.def_lexeme(
        headword="southeast",
        forms={
            WordForm.HEADWORD: "southeast",
            WordForm.COMPARATIVE: "further southeast",
            WordForm.SUPERLATIVE: "furthest southeast",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept, noun_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=southeast,
    )
    homer.def_concept_link(adj_concept, southeast_lexeme)
    homer.def_concept_link(noun_concept, southeast_lexeme)
    homer.def_concept_link(nsubj_concept, southeast_lexeme)
    homer.def_concept_link(pobj_concept, southeast_lexeme)
    midlands = homer.def_concept(
        name="midlands",
        locations=[Location([[2.5, 2]], location_space)],
        classifier=ProximityClassifier(),
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    midlands_lexeme = homer.def_lexeme(
        headword="midlands",
        forms={
            WordForm.HEADWORD: "midlands",
            WordForm.COMPARATIVE: "further inland",
            WordForm.SUPERLATIVE: "furthest inland",
        },
        parts_of_speech={
            WordForm.HEADWORD: [adj_concept, noun_concept],
            WordForm.COMPARATIVE: [adj_concept, jjr_concept],
            WordForm.SUPERLATIVE: [adj_concept],
        },
        parent_concept=midlands,
    )
    homer.def_concept_link(adj_concept, midlands_lexeme)
    homer.def_concept_link(noun_concept, midlands_lexeme)
    homer.def_concept_link(nsubj_concept, midlands_lexeme)
    homer.def_concept_link(pobj_concept, midlands_lexeme)
    the_lexeme = homer.def_lexeme(
        headword="the",
        forms={WordForm.HEADWORD: "the"},
        parts_of_speech={WordForm.HEADWORD: [det_concept]},
        parent_concept=None,
    )
    homer.def_concept_link(det_concept, midlands_lexeme)
    homer.def_concept_link(det_r_concept, midlands_lexeme)
    is_lexeme = homer.def_lexeme(
        headword="is",
        forms={WordForm.HEADWORD: "is"},
        parts_of_speech={WordForm.HEADWORD: [cop_concept]},
        parent_concept=None,
    )
    homer.def_concept_link(cop_concept, midlands_lexeme)
    homer.def_concept_link(cop_r_concept, midlands_lexeme)
    it_lexeme = homer.def_lexeme(
        headword="it",
        forms={WordForm.HEADWORD: "it"},
        parts_of_speech={WordForm.HEADWORD: [noun_concept]},
        parent_concept=None,
    )
    homer.def_concept_link(noun_concept, midlands_lexeme)
    homer.def_concept_link(nsubj_concept, midlands_lexeme)
    homer.def_concept_link(pobj_concept, midlands_lexeme)
    in_lexeme = homer.def_lexeme(
        headword="in",
        forms={WordForm.HEADWORD: "in"},
        parts_of_speech={WordForm.HEADWORD: [prep_concept]},
        parent_concept=None,
    )
    homer.def_concept_link(prep_concept, midlands_lexeme)
    homer.def_concept_link(prep_r_concept, midlands_lexeme)
    than_lexeme = homer.def_lexeme(
        headword="than",
        forms={WordForm.HEADWORD: "than"},
        parts_of_speech={WordForm.HEADWORD: [prep_concept]},
        parent_concept=None,
    )
    homer.def_concept_link(prep_concept, midlands_lexeme)
    homer.def_concept_link(prep_r_concept, midlands_lexeme)
    and_lexeme = homer.def_lexeme(
        headword="and",
        forms={WordForm.HEADWORD: "and"},
        parts_of_speech={WordForm.HEADWORD: [conj_concept]},
        parent_concept=None,
    )
    homer.def_concept_link(conj_concept, midlands_lexeme)
    comma_lexeme = homer.def_lexeme(
        headword=",",
        forms={WordForm.HEADWORD: ","},
        parts_of_speech={WordForm.HEADWORD: [conj_concept]},
        parent_concept=None,
    )
    homer.def_concept_link(conj_concept, midlands_lexeme)
    template_1 = homer.def_template(
        name="the [location] is [temperature]",
        parent_concept=text_concept,
        contents=[
            homer.def_word(the_lexeme),
            homer.def_word(word_form=WordForm.HEADWORD),
            homer.def_word(is_lexeme),
            homer.def_word(word_form=WordForm.HEADWORD),
        ],
    )
    template_1_location_space = location_space.instance_in_space(template_1)
    print(template_1_location_space)
    print(template_1_location_space.sub_spaces)
    homer.logger.log(template_1_location_space)
    template_1_temperature_space = temperature_space.instance_in_space(template_1)
    homer.logger.log(template_1_temperature_space)
    template_1_slot = homer.def_chunk(
        locations=[
            Location([], template_1),
            Location([[None, None]], template_1_location_space),
            Location([[None]], template_1_temperature_space),
        ],
        parent_space=template_1,
    )
    template_1_slot_location_label = homer.def_label(
        start=template_1_slot, parent_space=template_1_location_space
    )
    print("location label parent space:", template_1_slot_location_label.parent_space)
    template_1_slot_temperature_label = homer.def_label(
        start=template_1_slot, parent_space=template_1_temperature_space
    )
    print(
        "temperature label parent space:",
        template_1_slot_temperature_label.parent_space,
    )
    homer.def_correspondence(template_1_slot_location_label, template_1[1])
    homer.def_correspondence(template_1_slot_temperature_label, template_1[3])
    template_2 = homer.def_template(
        name="it is [temperature] in the [location]",
        parent_concept=text_concept,
        contents=[
            homer.def_word(it_lexeme),
            homer.def_word(is_lexeme),
            homer.def_word(word_form=WordForm.HEADWORD),
            homer.def_word(in_lexeme),
            homer.def_word(the_lexeme),
            homer.def_word(word_form=WordForm.HEADWORD),
        ],
    )
    template_2_location_space = location_space.instance_in_space(template_2)
    print(template_2_location_space)
    homer.logger.log(template_2_location_space)
    template_2_temperature_space = temperature_space.instance_in_space(template_2)
    homer.logger.log(template_2_temperature_space)
    template_2_slot = homer.def_chunk(
        locations=[
            Location([], template_2),
            Location([[None, None]], template_2_location_space),
            Location([[None]], template_2_temperature_space),
        ],
        parent_space=template_2,
    )
    template_2_slot_location_label = homer.def_label(
        start=template_2_slot, parent_space=template_2_location_space
    )
    template_2_slot_temperature_label = homer.def_label(
        start=template_2_slot, parent_space=template_2_temperature_space
    )
    homer.def_correspondence(template_2_slot_temperature_label, template_2[2])
    homer.def_correspondence(template_2_slot_location_label, template_2[5])
    template_3 = homer.def_template(
        name="it is [temperature.comparative] in the [location]",
        parent_concept=text_concept,
        contents=[
            homer.def_word(it_lexeme),
            homer.def_word(is_lexeme),
            homer.def_word(word_form=WordForm.COMPARATIVE),
            homer.def_word(in_lexeme),
            homer.def_word(the_lexeme),
            homer.def_word(word_form=WordForm.HEADWORD),
        ],
    )
    template_3_location_space = location_space.instance_in_space(template_3)
    homer.logger.log(template_3_location_space)
    template_3_temperature_space = temperature_space.instance_in_space(template_3)
    homer.logger.log(template_3_temperature_space)
    template_3_slot_1 = homer.def_chunk(
        locations=[
            Location([], template_3),
            Location([[None, None]], template_3_location_space),
            Location([[None]], template_3_temperature_space),
        ],
        parent_space=template_3,
    )
    template_3_slot_2 = homer.def_chunk(
        locations=[
            Location([], template_3),
            Location([[None, None]], template_3_location_space),
            Location([[None]], template_3_temperature_space),
        ],
        parent_space=template_3,
    )
    template_3_slot_1_location_label = homer.def_label(
        start=template_3_slot_1, parent_space=template_3_location_space
    )
    template_3_slots_temperature_relation = homer.def_relation(
        start=template_3_slot_1,
        end=template_3_slot_2,
        parent_space=template_3_temperature_space,
    )
    homer.def_correspondence(template_3_slots_temperature_relation, template_3[2])
    homer.def_correspondence(template_3_slot_1_location_label, template_3[5])
    template_4 = homer.def_template(
        name="it is [temperature.comparative] in the [location] than the [location]",
        parent_concept=text_concept,
        contents=[
            homer.def_word(it_lexeme),
            homer.def_word(is_lexeme),
            homer.def_word(word_form=WordForm.COMPARATIVE),
            homer.def_word(in_lexeme),
            homer.def_word(the_lexeme),
            homer.def_word(word_form=WordForm.HEADWORD),
            homer.def_word(than_lexeme),
            homer.def_word(the_lexeme),
            homer.def_word(word_form=WordForm.HEADWORD),
        ],
    )
    template_4_location_space = location_space.instance_in_space(template_4)
    homer.logger.log(template_4_location_space)
    template_4_temperature_space = temperature_space.instance_in_space(template_4)
    homer.logger.log(template_4_temperature_space)
    template_4_slot_1 = homer.def_chunk(
        locations=[
            Location([], template_4),
            Location([[None, None]], template_4_location_space),
            Location([[None]], template_4_temperature_space),
        ],
        parent_space=template_4,
    )
    template_4_slot_2 = homer.def_chunk(
        locations=[
            Location([], template_4),
            Location([[None, None]], template_4_location_space),
            Location([[None]], template_4_temperature_space),
        ],
        parent_space=template_4,
    )
    template_4_slot_1_location_label = homer.def_label(
        start=template_4_slot_1, parent_space=template_4_location_space
    )
    template_4_slot_2_location_label = homer.def_label(
        start=template_4_slot_2, parent_space=template_4_location_space
    )
    template_4_slots_temperature_relation = homer.def_relation(
        start=template_4_slot_1,
        end=template_4_slot_2,
        parent_space=template_4_temperature_space,
    )
    homer.def_correspondence(template_4_slots_temperature_relation, template_4[2])
    homer.def_correspondence(template_4_slot_1_location_label, template_4[5])
    homer.def_correspondence(template_4_slot_2_location_label, template_4[8])
    and_template = homer.def_template(
        name="[phrase] and [phrase]",
        parent_concept=discourse_concept,
        contents=[
            homer.def_phrase(label_concept=sentence_concept),
            homer.def_word(and_lexeme),
            homer.def_phrase(label_concept=sentence_concept),
        ],
    )
    list_template = homer.def_template(
        name="[phrase], [phrase]",
        parent_concept=discourse_concept,
        contents=[
            homer.def_phrase(label_concept=sentence_concept),
            homer.def_word(comma_lexeme),
            homer.def_phrase(label_concept=sentence_concept),
        ],
    )
    location_space_in_input = location_space.instance_in_space(input_space)
    homer.logger.log(location_space_in_input)
    temperature_space_in_input = temperature_space.instance_in_space(input_space)
    homer.logger.log(temperature_space_in_input)

    if True:
        input_chunks = StructureCollection()
        for i, row in enumerate(problem):
            for j, cell in enumerate(row):
                locations = [
                    Location([[i, j]], input_space),
                    Location([[i, j]], location_space_in_input),
                    Location([[cell]], temperature_space_in_input),
                ]
                members = StructureCollection()
                quality = 0.0
                chunk = Chunk(
                    ID.new(Chunk),
                    "",
                    locations,
                    members,
                    input_space,
                    quality,
                )
                logger.log(chunk)
                input_chunks.add(chunk)
                homer.bubble_chamber.chunks.add(chunk)
                input_space.add(chunk)
                location_space_in_input.add(chunk)
                temperature_space_in_input.add(chunk)

    if False:
        input_words = StructureCollection(
            {
                Word(
                    ID.new(Word),
                    "",
                    it_lexeme,
                    WordForm.HEADWORD,
                    Location([[0]], homer.bubble_chamber.spaces["input"]),
                    input_space,
                    1.0,
                ),
                Word(
                    ID.new(Word),
                    "",
                    is_lexeme,
                    WordForm.HEADWORD,
                    Location([[1]], homer.bubble_chamber.spaces["input"]),
                    input_space,
                    1.0,
                ),
                Word(
                    ID.new(Word),
                    "",
                    warm_lexeme,
                    WordForm.HEADWORD,
                    Location([[2]], homer.bubble_chamber.spaces["input"]),
                    input_space,
                    1.0,
                ),
                Word(
                    ID.new(Word),
                    "",
                    in_lexeme,
                    WordForm.HEADWORD,
                    Location([[3]], homer.bubble_chamber.spaces["input"]),
                    input_space,
                    1.0,
                ),
                Word(
                    ID.new(Word),
                    "",
                    the_lexeme,
                    WordForm.HEADWORD,
                    Location([[4]], homer.bubble_chamber.spaces["input"]),
                    input_space,
                    1.0,
                ),
                Word(
                    ID.new(Word),
                    "",
                    south_lexeme,
                    WordForm.HEADWORD,
                    Location([[5]], homer.bubble_chamber.spaces["input"]),
                    input_space,
                    1.0,
                ),
            }
        )
        for word in input_words:
            homer.logger.log(word)
            homer.bubble_chamber.words.add(word)
            input_space.add(word)

    return homer


for _ in range(1):
    homer = setup_homer()
    result = homer.run()
    with open("results.csv", "a") as f:
        f.write(str(result["codelets_run"]) + "\n")
