from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'remove all expired otp codes'

    def handle(self, *args, **options):
        expiration_time = datetime.now() - timedelta(minutes=2)
        expired_otps = OtpCode.objects.filter(created__lt=expiration_time)
        expired_otps.delete()
        self.stdout.write(self.style.SUCCESS('Successfully removed expired OTP codes.'))