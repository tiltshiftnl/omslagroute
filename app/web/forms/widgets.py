from django.forms import RadioSelect as DefaultRadioSelect
from django.forms.widgets import ClearableFileInput as DefaultClearableFileInput, CheckboxSelectMultiple as DefaultCheckboxSelectMultiple


class RadioSelect(DefaultRadioSelect):
    template_name = 'forms/radios.html'
    option_template_name = 'forms/inputs.html'


class ClearableFileInput(DefaultClearableFileInput):
    template_name = 'forms/clearable_file_input.html'


class CheckboxSelectMultiple(DefaultCheckboxSelectMultiple):
    template_name = 'forms/checkbox_select.html'
    option_template_name = 'forms/checkbox_option.html'
