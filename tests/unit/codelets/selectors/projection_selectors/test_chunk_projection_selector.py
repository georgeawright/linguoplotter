import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.selectors.projection_selectors import ChunkProjectionSelector
from homer.structure_collection import StructureCollection


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"chunk": Mock(), "select": Mock()}
    return chamber


def test_word_is_boosted(bubble_chamber):
    chunk = Mock()
    chunk.size = 1
    chunk.quality = 1.0
    chunk.activation = 0.0

    parent_concept = Mock()
    correspondence_from_frame = Mock()
    correspondence_from_frame.is_correspondence = True
    correspondence_from_frame.start.parent_space.is_frame = True
    correspondence_from_frame.start.parent_space.parent_concept = parent_concept
    correspondence_from_frame.end.parent_space.parent_concept = parent_concept
    correspondence_from_frame.quality = 1.0
    correspondence_from_frame.activation = 1.0

    selector = ChunkProjectionSelector(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({chunk, correspondence_from_frame}),
        Mock(),
    )
    selector.run()
    assert CodeletResult.SUCCESS == selector.result
    assert chunk.boost_activation.is_called()