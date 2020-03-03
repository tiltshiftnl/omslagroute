from django.forms.widgets import *


class DocumentCheckboxSelectMultiple(CheckboxSelectMultiple):
    option_template_name = 'form/checkbox_option.html'
    template_name = 'form/checkbox_list.html'
