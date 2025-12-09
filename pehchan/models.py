from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import EmailValidator


class Event(models.Model):
    """Model for managing events"""
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.name} - {self.event_date}"


class EventVolunteer(models.Model):
    """Model for event-specific volunteers"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_volunteers')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='volunteers')
    joined_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        unique_together = ['user', 'event']
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.name}"


class LifetimeVolunteer(models.Model):
    """Model for lifetime volunteers"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lifetime_volunteer')
    joined_at = models.DateTimeField(auto_now_add=True)
    motivation = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_lifetime_volunteers')
    
    class Meta:
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} - Lifetime Volunteer ({self.get_status_display()})"


class Certificate(models.Model):
    """Model for volunteer certificates"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='certificates')
    volunteer = models.ForeignKey(EventVolunteer, on_delete=models.CASCADE, related_name='certificates')
    certificate_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    issue_date = models.DateField(default=timezone.now)
    file = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    class Meta:
        unique_together = ['event', 'volunteer']
        ordering = ['-issue_date']
    
    def save(self, *args, **kwargs):
        # Auto-generate certificate number if not exists
        if not self.certificate_number:
            import random
            import string
            year = timezone.now().year
            random_str = ''.join(random.choices(string.digits, k=6))
            self.certificate_number = f"CERT-{year}-{random_str}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Certificate {self.certificate_number or f'#{self.pk}'} - {self.volunteer.user.username} - {self.event.name}"


class MaterialDonation(models.Model):
    """Model for material donations"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('processed', 'Processed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_donations')
    item_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    location = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.item_name}"
    
    def get_pickup_message(self):
        if self.location.lower() == 'mumbai':
            return "Pehchan team will pick up your material."
        else:
            return "Please courier your material to our office."


class MoneyDonation(models.Model):
    """Model for money donations"""
    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='money_donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='upi')
    upi_id = models.CharField(max_length=100, blank=True)
    receipt_upload = models.FileField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - ₹{self.amount}"


class DonorCertificate(models.Model):
    """Model for donor certificates"""
    DONATION_TYPE_CHOICES = [
        ('material', 'Material Donation'),
        ('money', 'Money Donation'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor_certificates')
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE_CHOICES)
    material_donation = models.ForeignKey(
        MaterialDonation, 
        on_delete=models.CASCADE, 
        related_name='certificates',
        blank=True,
        null=True
    )
    money_donation = models.ForeignKey(
        MoneyDonation, 
        on_delete=models.CASCADE, 
        related_name='certificates',
        blank=True,
        null=True
    )
    
    # Certificate details
    certificate_number = models.CharField(max_length=50, unique=True, editable=False)
    issue_date = models.DateField(default=timezone.now)
    issued_by = models.CharField(max_length=200, default='Pehchan NGO')
    remarks = models.TextField(blank=True, help_text='Additional remarks or appreciation message')
    
    # Optional file attachment
    file = models.FileField(upload_to='donor_certificates/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issue_date', '-created_at']
        verbose_name = 'Donor Certificate'
        verbose_name_plural = 'Donor Certificates'
    
    def save(self, *args, **kwargs):
        # Auto-generate certificate number if not exists
        if not self.certificate_number:
            import random
            import string
            year = timezone.now().year
            random_str = ''.join(random.choices(string.digits, k=6))
            self.certificate_number = f"DON-{year}-{random_str}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.user.username}"
    
    def get_donation_details(self):
        """Get the related donation details"""
        if self.donation_type == 'material' and self.material_donation:
            return f"{self.material_donation.item_name} (Qty: {self.material_donation.quantity})"
        elif self.donation_type == 'money' and self.money_donation:
            return f"₹{self.money_donation.amount}"
        return "N/A"
    
    def get_donation_date(self):
        """Get the date of donation"""
        if self.donation_type == 'material' and self.material_donation:
            return self.material_donation.created_at
        elif self.donation_type == 'money' and self.money_donation:
            return self.money_donation.created_at
        return None


class AnonymousDonation(models.Model):
    """Model for anonymous donations without login"""
    # Donor Information (Optional)
    donor_name = models.CharField(max_length=200, blank=True, null=True, help_text='Donor name (optional for anonymous)')
    donor_email = models.EmailField(blank=True, null=True, help_text='Email for receipt (optional)')
    donor_phone = models.CharField(max_length=20, blank=True, null=True, help_text='Contact number (optional)')
    
    # Donation Details
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Donation amount')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text='UPI transaction ID')
    
    # Receipt
    receipt = models.FileField(upload_to='anonymous_donation_receipts/', blank=True, null=True, help_text='Upload payment receipt')
    
    # Receipt Preference
    wants_receipt = models.BooleanField(default=False, help_text='Donor wants a receipt marked as Anonymous')
    
    # Additional Information
    message = models.TextField(blank=True, null=True, help_text='Additional message from donor')
    
    # Google Form Submission URL (for reference)
    google_form_submitted = models.BooleanField(default=False, help_text='Has the donor submitted the Google Form?')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text='IP address of donor')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Anonymous Donation'
        verbose_name_plural = 'Anonymous Donations'
    
    def __str__(self):
        donor = self.donor_name if self.donor_name else 'Anonymous'
        return f"{donor} - ₹{self.amount} - {self.created_at.strftime('%Y-%m-%d')}"


class ContactMessage(models.Model):
    """Model for contact form messages from website visitors"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Contact Information
    name = models.CharField(max_length=200, help_text='Full name of the person')
    email = models.EmailField(validators=[EmailValidator()], help_text='Email address for response')
    
    # Message Details
    message = models.TextField(help_text='Message content')
    
    # Status & Priority
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        help_text='Current status of the message'
    )
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        help_text='Priority level for handling this message'
    )
    
    # Admin Notes
    admin_notes = models.TextField(
        blank=True, 
        null=True,
        help_text='Internal notes for team members (not visible to sender)'
    )
    
    # Response
    response = models.TextField(
        blank=True, 
        null=True,
        help_text='Response sent to the person'
    )
    responded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='contact_responses',
        help_text='Admin who responded to this message'
    )
    responded_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text='Date and time when response was sent'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True,
        help_text='IP address of the sender (for security)'
    )
    user_agent = models.TextField(
        blank=True, 
        null=True,
        help_text='Browser information (for analytics)'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def mark_as_read(self):
        """Mark message as read"""
        if self.status == 'new':
            self.status = 'read'
            self.save()
    
    def mark_as_replied(self, user=None):
        """Mark message as replied"""
        self.status = 'replied'
        if user:
            self.responded_by = user
        self.responded_at = timezone.now()
        self.save()
    
    def get_short_message(self, length=50):
        """Get shortened message for display"""
        if len(self.message) > length:
            return f"{self.message[:length]}..."
        return self.message


class PasswordResetOTP(models.Model):
    """Model to store OTP for password reset"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def is_valid(self):
        """Check if OTP is still valid"""
        from django.utils import timezone
        return timezone.now() < self.expires_at
    
    def __str__(self):
        return f"OTP for {self.user.username}"


class PehchanWallet(models.Model):
    """Model for Pehchan Wallet to track organization funds"""
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pehchan Wallet'
        verbose_name_plural = 'Pehchan Wallet'
    
    def __str__(self):
        return f"Pehchan Wallet - Balance: ₹{self.balance}"
    
    @classmethod
    def get_wallet(cls):
        """Get or create the single wallet instance"""
        wallet, created = cls.objects.get_or_create(id=1)
        return wallet
    
    def deposit(self, amount, description="", transaction_type="donation"):
        """Deposit money to wallet"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        self.save()
        
        # Create transaction record
        return WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            balance_after_transaction=self.balance
        )
    
    def withdraw(self, amount, description="", transaction_type="expense"):
        """Withdraw money from wallet"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.balance:
            raise ValueError("Insufficient funds in wallet")
        
        self.balance -= amount
        self.save()
        
        # Create transaction record
        return WalletTransaction.objects.create(
            wallet=self,
            amount=-amount,  # Negative for withdrawals
            transaction_type=transaction_type,
            description=description,
            balance_after_transaction=self.balance
        )


class WalletTransaction(models.Model):
    """Model to track all wallet transactions"""
    TRANSACTION_TYPES = [
        ('donation', 'Donation'),
        ('expense', 'Expense'),
        ('adjustment', 'Adjustment'),
    ]
    
    wallet = models.ForeignKey(PehchanWallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Positive for deposits, negative for withdrawals")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)
    related_donation = models.ForeignKey(
        MoneyDonation, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='wallet_transactions'
    )
    related_expense = models.ForeignKey(
        'Expense', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='wallet_transactions'
    )
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wallet Transaction'
        verbose_name_plural = 'Wallet Transactions'
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - ₹{abs(self.amount)} - {self.created_at.strftime('%Y-%m-%d')}"


class Expense(models.Model):
    """Model for tracking organization expenses"""
    CATEGORY_CHOICES = [
        ('office', 'Office Supplies'),
        ('travel', 'Travel'),
        ('salary', 'Salary'),
        ('marketing', 'Marketing'),
        ('utilities', 'Utilities'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    receipt = models.FileField(upload_to='expenses/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='expenses_created')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses_approved')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
    
    def __str__(self):
        return f"{self.title} - ₹{self.amount} - {self.date}"
