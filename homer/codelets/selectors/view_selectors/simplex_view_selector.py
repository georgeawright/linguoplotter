from homer.codelets.selectors import ViewSelector
from homer.structures.views import SimplexView


class SimplexViewSelector(ViewSelector):
    @classmethod
    def get_target_class(cls):
        return SimplexView