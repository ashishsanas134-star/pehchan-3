from unittest.mock import MagicMock
import os
import sys

# Isolated test
class MockQuerySet:
    def __init__(self, last_number=None):
        self.last_number = last_number
    def filter(self, **kwargs): return self
    def order_by(self, *args): return self
    def first(self):
        if self.last_number:
            return MagicMock(certificate_number=self.last_number)
        return None
    def exists(self): return False

def generate_cert_number(model_class, prefix):
    last_cert = model_class.objects.filter(
        certificate_number__startswith=prefix
    ).order_by('-certificate_number').first()
    
    if last_cert:
        try:
            last_sequence = int(last_cert.certificate_number.split('/')[-1])
            new_sequence = last_sequence + 1
        except (ValueError, IndexError):
            new_sequence = 1
    else:
        new_sequence = 1
        
    return f"{prefix}{new_sequence:04d}"

# Test Donor (D)
mock_donor = MagicMock()
mock_donor.objects = MockQuerySet("PYUI/2026/D/0005")
print(f"Next Donor Cert: {generate_cert_number(mock_donor, 'PYUI/2026/D/')}")

# Test Volunteer (V)
mock_vol = MagicMock()
mock_vol.objects = MockQuerySet("PYUI/2026/V/0012")
print(f"Next Vol Cert: {generate_cert_number(mock_vol, 'PYUI/2026/V/')}")

# Test First (None)
mock_first = MagicMock()
mock_first.objects = MockQuerySet(None)
print(f"First Cert: {generate_cert_number(mock_first, 'PYUI/2026/V/')}")
