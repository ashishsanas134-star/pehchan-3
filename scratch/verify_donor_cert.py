import os
import sys
import django
from unittest.mock import MagicMock

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pehchan_webapp.settings')
os.environ.setdefault('SECRET_KEY', 'fake-key-for-verification')
os.environ.setdefault('DEBUG', 'True')

# Mock cloudinary before django.setup()
sys.modules['cloudinary_storage'] = MagicMock()
sys.modules['cloudinary_storage.storage'] = MagicMock()
sys.modules['cloudinary_storage.management.commands.collectstatic'] = MagicMock()

try:
    django.setup()
    from pehchan.models import DonorCertificate, User, MaterialDonation, MoneyDonation
    from django.utils import timezone

    print("Django setup successful.")

    # Create a mock user
    user = User(username="testuser", email="test@example.com")
    
    # Test Material Donation Certificate Details
    mat_donation = MaterialDonation(
        user=user, 
        item_name="Clothes", 
        quantity=5, 
        location="Delhi",
        created_at=timezone.now()
    )
    cert_mat = DonorCertificate(
        user=user,
        donation_type='material',
        material_donation=mat_donation,
        certificate_number="DON-2024-123456"
    )
    print(f"Material details: {cert_mat.get_donation_details()}")

    # Test Money Donation Certificate Details
    mon_donation = MoneyDonation(
        user=user,
        amount=1000,
        payment_method='upi',
        created_at=timezone.now()
    )
    cert_mon = DonorCertificate(
        user=user,
        donation_type='money',
        money_donation=mon_donation,
        certificate_number="DON-2024-654321"
    )
    print(f"Money details: {cert_mon.get_donation_details()}")

    # Test string representation
    print(f"String representation: {cert_mon}")

except Exception as e:
    print(f"Verification failed: {e}")
    import traceback
    traceback.print_exc()
