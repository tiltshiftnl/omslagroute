from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--username', dest='username', default=None,
            help='Specifies the username for the superuser.',
        )
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        userModel = get_user_model()
        if userModel.objects.count() == 0:
            email = '%s@meail.com' % options.get('username')
            password = options.get('password')
            username = options.get('username')
            print('Creating account for %s (%s)' % (username, email))
            admin = userModel.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
