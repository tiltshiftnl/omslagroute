from django.forms import RadioSelect as DefaultRadioSelect


class RadioSelect(DefaultRadioSelect):
    template_name = 'forms/radios.html'
    option_template_name = 'forms/inputs.html'
