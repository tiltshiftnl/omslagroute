from django.forms import RadioSelect as DefaultRadioSelect
from django.forms.widgets import \
    ClearableFileInput as DefaultClearableFileInput, \
    CheckboxSelectMultiple as DefaultCheckboxSelectMultiple


class RadioSelect(DefaultRadioSelect):
    template_name = 'forms/radios.html'
    option_template_name = 'forms/inputs.html'


class ClearableFileInput(DefaultClearableFileInput):
    template_name = 'forms/clearable_file_input.html'


class CheckboxSelectMultiple(DefaultCheckboxSelectMultiple):
    template_name = 'forms/checkbox_select.html'
    option_template_name = 'forms/checkbox_option.html'


class CheckboxSelectMultipleUser(DefaultCheckboxSelectMultiple):
    template_name = 'forms/checkbox_select_user.html'
    option_template_name = 'forms/checkbox_option_user.html'


class CheckboxSelectMultipleDocument(DefaultCheckboxSelectMultiple):
    template_name = 'forms/checkbox_select_document.html'
    option_template_name = 'forms/checkbox_option_document.html'

    def get_context(self, name, value, attrs):
        attrs.update(self.attrs)
        return super().get_context(name, value, attrs)
