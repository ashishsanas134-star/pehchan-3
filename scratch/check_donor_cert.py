import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pehchan_webapp.settings')
os.environ['DEBUG'] = 'True'
os.environ['SECRET_KEY'] = 'fake-key-for-script'

# Pre-setup hook to mock missing apps
import sys
from unittest.mock import MagicMock

# Mock cloudinary_storage and cloudinary
sys.modules["cloudinary_storage"] = MagicMock()
sys.modules["cloudinary_storage.storage"] = MagicMock()
sys.modules["cloudinary"] = MagicMock()

django.setup()

from pehchan.models import DonorCertificate

print("Checking DonorCertificate records...")
for cert in DonorCertificate.objects.all():
    try:
        print(f"ID: {cert.id}, Number: {cert.certificate_number}, User: {cert.user.username}, Type: {cert.donation_type}")
        print(f"  Details: {cert.get_donation_details()}")
    except Exception as e:
        print(f"  ERROR on ID {cert.id}: {str(e)}")

print("\nChecking for missing fields in admin...")
from pehchan.admin import DonorCertificateAdmin
from django.contrib.admin.sites import AdminSite

site = AdminSite()
admin = DonorCertificateAdmin(DonorCertificate, site)
print(f"List display: {admin.list_display}")
print(f"Readonly fields: {admin.readonly_fields}")
