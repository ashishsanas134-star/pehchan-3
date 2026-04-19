from unittest.mock import MagicMock

class MockModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def get_donation_details(obj):
    try:
        if obj.donation_type == 'material' and obj.material_donation:
            return f"{obj.material_donation.item_name} (Qty: {obj.material_donation.quantity})"
        elif obj.donation_type == 'money' and obj.money_donation:
            return f"Rs. {obj.money_donation.amount}"
    except Exception:
        return "Error retrieving details"
    return "N/A"

# Test Material
mat_donation = MockModel(item_name="Clothes", quantity=5)
cert_mat = MockModel(donation_type='material', material_donation=mat_donation)
print(f"Material details: {get_donation_details(cert_mat)}")

# Test Money
mon_donation = MockModel(amount=1000)
cert_mon = MockModel(donation_type='money', money_donation=mon_donation)
print(f"Money details: {get_donation_details(cert_mon)}")

# Test N/A
cert_na = MockModel(donation_type='other', material_donation=None, money_donation=None)
print(f"N/A details: {get_donation_details(cert_na)}")

# Test Error
cert_err = MockModel(donation_type='money', money_donation=None) # Should trigger exception or return N/A
print(f"Error details: {get_donation_details(cert_err)}")
