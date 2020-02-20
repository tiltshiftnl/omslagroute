from django.conf import settings



def app_settings(request=None):
    return {
        'SOURCE_COMMIT': settings.SOURCE_COMMIT,
    }
