from django.views.generic import FormView
from .forms import *
from constance import config
from django.http.response import HttpResponseRedirect
import sendgrid
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from sendgrid.helpers.mail import Mail


def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


class FeedbackFormView(FormView):
    form_class = FeedbackForm
    template_name = 'feedback/feedback.html'
    success_url = '.?send=1'

    def form_valid(self, form):
        addresses = [x.strip() for x in config.FEEDBACK_RECIPIENT_LIST.split(',') if validateEmail(x.strip())]
        if addresses:
            current_site = get_current_site(self.request)
            # sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
            # body = ''
            # email = Mail(
            #     from_email='no-reply@%s' % current_site.domain,
            #     to_emails=addresses,
            #     subject='Omslagroute - feedback',
            #     plain_text_content=body
            # )
            # sg.send(email)
        else:
            return HttpResponseRedirect('./?error=1')
        return super().form_valid(form)
