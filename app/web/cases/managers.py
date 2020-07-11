from django.db import models
from web.users.statics import *
import datetime
from constance import config


class CaseManager(models.Manager):
    def by_user(self, user):
        from .models import CaseVersion
        datetime_treshold = datetime.datetime.now() - datetime.timedelta(seconds=config.CASE_DELETE_SECONDS)
        queryset = self.get_queryset()

        if user.user_type in [BEGELEIDER, PB_FEDERATIE_BEHEERDER]:
            queryset = queryset.filter(
                id__in=user.profile.cases.all().values_list('id', flat=True)
            ).exclude(
                delete_request_date__lte=datetime_treshold
            ).order_by('-saved')
            return queryset
        if user.user_type in [WONINGCORPORATIE_MEDEWERKER]:
            queryset = queryset.filter(
                woningcorporatie_medewerker__user__federation=user.federation,
            )
            return queryset
        return queryset.filter(
            id__in=CaseVersion.objects.order_by('case').distinct().values_list('case'),
            delete_request_date__isnull=True,
        )