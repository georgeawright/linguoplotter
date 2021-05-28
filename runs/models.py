from django.db import models

MAX_STRING_LENGTH = 200


class RunRecord(models.Model):
    start_time = models.DateTimeField("Completion Time", auto_now_add=True)


class CodeletRecord(models.Model):
    codelet_id = models.CharField("Codelet ID", max_length=MAX_STRING_LENGTH)
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE)
    codelet_type = models.CharField("Codelet Type", max_length=MAX_STRING_LENGTH)
    birth_time = models.IntegerField("Birth Time")
    time_run = models.IntegerField("Time Run", blank=True, null=True)
    urgency = models.FloatField("Urgency")
    result = models.IntegerField("Result", blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    target_structures = models.ManyToManyField(
        "StructureRecord",
        blank=True,
        null=True,
    )
    champion = models.ForeignKey(
        "StructureRecord",
        related_name="champion",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    challenger = models.ForeignKey(
        "StructureRecord",
        related_name="challenger",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    follow_up = models.ForeignKey(
        "self",
        related_name="Follow Up Codelet+",
        on_delete=models.CASCADE,
        unique=True,
        blank=True,
        null=True,
    )


class CoderackRecord(models.Model):
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE, unique=True)
    codelets_run = models.JSONField("Codelets Run")
    population = models.JSONField("Population")
    satisfaction = models.JSONField("Satisfaction")
    result = models.CharField(
        "result", max_length=MAX_STRING_LENGTH, blank=True, null=True
    )


class EventRecord(models.Model):
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE)
    event_time = models.IntegerField("Birth Time")
    event_type = models.CharField("Codelet ID", max_length=MAX_STRING_LENGTH)
    codelet = models.ForeignKey("CodeletRecord", on_delete=models.CASCADE)
    target_structures = models.ManyToManyField(
        "StructureRecord",
        related_name="_target_structures",
        blank=True,
        null=True,
    )
    child_structures = models.ManyToManyField(
        "StructureRecord",
        related_name="_child_structures",
        blank=True,
        null=True,
    )
    winner = models.ForeignKey(
        "StructureRecord",
        related_name="_winner",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    loser = models.ForeignKey(
        "StructureRecord",
        related_name="_loser",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class StructureRecord(models.Model):
    structure_id = models.CharField("Structure ID", max_length=MAX_STRING_LENGTH)
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE)
    time_created = models.IntegerField("Time Created")
    value = models.CharField("Value", max_length=MAX_STRING_LENGTH, null=True)
    locations = models.JSONField("location", blank=True, null=True)
    no_of_dimensions = models.IntegerField("No of Dimensions", blank=True, null=True)
    is_basic_level = models.BooleanField("Is basic level", blank=True, null=True)
    links = models.ManyToManyField("self", blank=True, null=True)
    members = models.ManyToManyField("self", blank=True, null=True)
    contents = models.ManyToManyField("self", blank=True, null=True)
    dimensions = models.ManyToManyField("self", blank=True, null=True)
    sub_spaces = models.ManyToManyField("self", blank=True, null=True)
    input_spaces = models.ManyToManyField("self", blank=True, null=True)
    output_space = models.ForeignKey(
        "StructureRecord",
        related_name="_output_space",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    conceptual_space = models.ForeignKey(
        "StructureRecord",
        related_name="_conceptual_space",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    activation = models.JSONField("Activation")
    unhappiness = models.JSONField("Unhappiness")
    quality = models.JSONField("quality")
    parent_concept = models.ForeignKey(
        "StructureRecord",
        related_name="_parent_concept",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    parent_space = models.ForeignKey(
        "StructureRecord",
        related_name="_parent_space",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    parent_codelet = models.ForeignKey(
        "CodeletRecord", on_delete=models.CASCADE, blank=True, null=True
    )
    start = models.ForeignKey(
        "StructureRecord",
        related_name="start_arg",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    end = models.ForeignKey(
        "StructureRecord",
        related_name="end_arg",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    left_branch = models.ForeignKey(
        "StructureRecord",
        related_name="_left_branch",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    right_branch = models.ForeignKey(
        "StructureRecord",
        related_name="_right_branch",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class StructureUpdateRecord(models.Model):
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE)
    time = models.IntegerField("Time")
    codelet = models.ForeignKey("CodeletRecord", on_delete=models.CASCADE)
    structure = models.ForeignKey("StructureRecord", on_delete=models.CASCADE)
    action = models.CharField("Action", max_length=MAX_STRING_LENGTH)
