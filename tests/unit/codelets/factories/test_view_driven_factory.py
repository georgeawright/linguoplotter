import pytest
from unittest.mock import Mock

from linguoplotter.codelets.factories import ViewDrivenFactory
from linguoplotter.codelets.suggesters import (
    ChunkSuggester,
    LabelSuggester,
    RelationSuggester,
)
from linguoplotter.structure_collection import StructureCollection


# TODO
