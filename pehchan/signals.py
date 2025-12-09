from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import MoneyDonation, Expense, PehchanWallet


@receiver(post_save, sender=MoneyDonation)
def handle_donation_wallet_transaction(sender, instance, created, **kwargs):
    """Automatically deposit money to wallet when a money donation is made"""
    if created:
        wallet = PehchanWallet.get_wallet()
        wallet.deposit(
            amount=instance.amount,
            description=f"Donation from {instance.user.get_full_name() or instance.user.username}",
            transaction_type="donation"
        )


@receiver(post_save, sender=Expense)
def handle_expense_wallet_transaction(sender, instance, created, **kwargs):
    """Automatically withdraw money from wallet when an expense is created"""
    if created:
        wallet = PehchanWallet.get_wallet()
        wallet.withdraw(
            amount=instance.amount,
            description=f"Expense: {instance.title}",
            transaction_type="expense"
        )