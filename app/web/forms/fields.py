from multiselectfield import MultiSelectFormField as DefaultMultiSelectFormField
from .widgets import CheckboxSelectMultiple


class MultiSelectFormField(DefaultMultiSelectFormField):
    widget = CheckboxSelectMultiple
