from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(
        label='Naam',
        required=False,
    )
    email = forms.EmailField(
        label='E-mailadres',
        required=False,
    )
    feedback = forms.CharField(
        label='Wat wil je ons laten weten',
        required=True,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
            }
        ),
    )
