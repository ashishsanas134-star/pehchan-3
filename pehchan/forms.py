from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import EventVolunteer, LifetimeVolunteer, MaterialDonation, MoneyDonation, ContactMessage, AnonymousDonation


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class EventVolunteerForm(forms.ModelForm):
    class Meta:
        model = EventVolunteer
        fields = []
        

class LifetimeVolunteerForm(forms.ModelForm):
    class Meta:
        model = LifetimeVolunteer
        fields = ['motivation']
        widgets = {
            'motivation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us why you want to become a lifetime volunteer...'
            }),
        }


class MaterialDonationForm(forms.ModelForm):
    class Meta:
        model = MaterialDonation
        fields = ['item_name', 'quantity', 'location', 'message']
        widgets = {
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item Name'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantity',
                'min': 1
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Location'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional message (optional)'
            }),
        }


class MoneyDonationForm(forms.ModelForm):
    receipt_upload = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*,.pdf'
        })
    )

    class Meta:
        model = MoneyDonation
        fields = ['amount', 'receipt_upload']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount in ₹',
                'min': 1,
                'step': '0.01'
            }),
        }


class CertificateVerificationForm(forms.Form):
    certificate_id = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'certificate_id',  # Explicitly set the ID
            'placeholder': 'Enter Certificate ID (e.g. VOL-2024-001)'
        })
    )


class ContactMessageForm(forms.ModelForm):
    """Form for contact messages from home page"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Message',
                'rows': 5,
                'required': True
            }),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'message': 'Your Message'
        }


class AnonymousDonationForm(forms.ModelForm):
    """Form for anonymous donations"""
    class Meta:
        model = AnonymousDonation
        fields = ['donor_name', 'donor_email', 'donor_phone', 'amount', 'transaction_id', 'receipt', 'wants_receipt', 'message']
        widgets = {
            'donor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name (Optional)',
            }),
            'donor_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email (Optional - for receipt)',
            }),
            'donor_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number (Optional)',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount Donated (₹)',
                'min': 1,
                'step': '0.01',
                'required': True
            }),
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UPI Transaction ID (Optional)',
            }),
            'receipt': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
            'wants_receipt': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Message (Optional)',
                'rows': 3,
            }),
        }
        labels = {
            'donor_name': 'Name',
            'donor_email': 'Email',
            'donor_phone': 'Phone',
            'amount': 'Donation Amount',
            'transaction_id': 'Transaction ID',
            'receipt': 'Payment Receipt',
            'wants_receipt': 'I want a receipt marked as "Anonymous"',
            'message': 'Message'
        }


class ForgotPasswordForm(forms.Form):
    """Form for entering email to reset password"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'required': True
        })
    )


class OTPVerificationForm(forms.Form):
    """Form for entering OTP"""
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit OTP',
            'required': True
        })
    )


class ResetPasswordForm(forms.Form):
    """Form for resetting password"""
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password',
            'required': True
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password',
            'required': True
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
