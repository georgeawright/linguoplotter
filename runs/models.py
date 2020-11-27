from django.db import models

MAX_STRING_LENGTH = 200


class RunRecord(models.Model):
    start_time = models.DateTimeField("Completion Time", auto_now_add=True)


class CodeletRecord(models.Model):
    codelet_id = models.CharField("Codelet ID", max_length=MAX_STRING_LENGTH)
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE)
    codelet_type = models.CharField("Codelet ID", max_length=MAX_STRING_LENGTH)
    birth_time = models.IntegerField("Birth Time")
    time_run = models.IntegerField("Time Run", blank=True, null=True)
    urgency = models.FloatField("Urgency")
    parent = models.ForeignKey(
        "self",
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    target_structure = models.ForeignKey(
        "StructureRecord", on_delete=models.CASCADE, blank=True, null=True
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


class StructureRecord(models.Model):
    structure_id = models.CharField("Structure ID", max_length=MAX_STRING_LENGTH)
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE)
    time_created = models.IntegerField("Time Created")
    value = models.CharField("Value", max_length=MAX_STRING_LENGTH)
    location = models.JSONField("location", null=True)
    links = models.ManyToManyField("self", blank=True, null=True)
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


class StructureUpdateRecord(models.Model):
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE)
    time = models.IntegerField("Time")
    codelet = models.ForeignKey("CodeletRecord", on_delete=models.CASCADE)
    structure = models.ForeignKey("StructureRecord", on_delete=models.CASCADE)
    action = models.CharField("Action", max_length=MAX_STRING_LENGTH)
