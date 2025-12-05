from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import (
    Event, EventVolunteer, LifetimeVolunteer, 
    Certificate, MaterialDonation, MoneyDonation, DonorCertificate, ContactMessage, AnonymousDonation
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_date', 'location', 'status', 'created_at']
    list_filter = ['status', 'event_date']
    search_fields = ['name', 'location', 'description']
    date_hierarchy = 'event_date'
    ordering = ['-event_date']


@admin.register(EventVolunteer)
class EventVolunteerAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'joined_at', 'status']
    list_filter = ['status', 'joined_at', 'event']
    search_fields = ['user__username', 'user__email', 'event__name']
    date_hierarchy = 'joined_at'
    ordering = ['-joined_at']


@admin.register(LifetimeVolunteer)
class LifetimeVolunteerAdmin(admin.ModelAdmin):
    list_display = ['user', 'joined_at']
    search_fields = ['user__username', 'user__email', 'motivation']
    date_hierarchy = 'joined_at'
    ordering = ['-joined_at']
    readonly_fields = ['joined_at']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_id', 'volunteer', 'event', 'issue_date']
    list_filter = ['issue_date', 'event']
    search_fields = ['volunteer__user__username', 'event__name']
    date_hierarchy = 'issue_date'
    ordering = ['-issue_date']
    
    def certificate_id(self, obj):
        return obj.pk
    certificate_id.short_description = 'Certificate ID'


@admin.register(MaterialDonation)
class MaterialDonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_name', 'quantity', 'location', 'status', 'created_at']
    list_filter = ['status', 'location', 'created_at']
    search_fields = ['user__username', 'item_name', 'location']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(MoneyDonation)
class MoneyDonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'created_at']
    list_filter = ['payment_method', 'created_at']
    search_fields = ['user__username', 'user__email', 'upi_id']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(DonorCertificate)
class DonorCertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_number', 'user', 'donation_type', 'get_donation_info', 'issue_date', 'created_at']
    list_filter = ['donation_type', 'issue_date', 'created_at']
    search_fields = ['certificate_number', 'user__username', 'user__email', 'user__first_name', 'user__last_name']
    date_hierarchy = 'issue_date'
    ordering = ['-issue_date', '-created_at']
    readonly_fields = ['certificate_number', 'created_at', 'updated_at', 'get_donation_preview']
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('user', 'donation_type')
        }),
        ('Donation Details', {
            'fields': ('material_donation', 'money_donation', 'get_donation_preview')
        }),
        ('Certificate Information', {
            'fields': ('certificate_number', 'issue_date', 'issued_by', 'remarks', 'file')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_donation_info(self, obj):
        """Display donation details in list view"""
        return obj.get_donation_details()
    get_donation_info.short_description = 'Donation Details'
    
    def get_donation_preview(self, obj):
        """Show donation preview in admin form"""
        if obj.donation_type == 'material' and obj.material_donation:
            donation = obj.material_donation
            return f"Item: {donation.item_name} | Quantity: {donation.quantity} | Location: {donation.location} | Date: {donation.created_at.strftime('%Y-%m-%d')}"
        elif obj.donation_type == 'money' and obj.money_donation:
            donation = obj.money_donation
            return f"Amount: ₹{donation.amount} | Payment Method: {donation.get_payment_method_display()} | Date: {donation.created_at.strftime('%Y-%m-%d')}"
        return "No donation selected"
    get_donation_preview.short_description = 'Donation Preview'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter donation options based on donation_type"""
        if db_field.name == "material_donation":
            # Show only material donations
            kwargs["queryset"] = MaterialDonation.objects.select_related('user').all()
        elif db_field.name == "money_donation":
            # Show only money donations
            kwargs["queryset"] = MoneyDonation.objects.select_related('user').all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    class Media:
        js = ('admin/js/donor_certificate_admin.js',)
        css = {
            'all': ('admin/css/donor_certificate_admin.css',)
        }


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'colored_status', 
        'name', 
        'email', 
        'short_message_display', 
        'priority_badge',
        'created_at',
        'responded_by',
        'action_buttons'
    ]
    
    list_filter = [
        'status',
        'priority', 
        'created_at',
        'responded_at',
        'responded_by',
        ('created_at', admin.DateFieldListFilter),
    ]
    
    search_fields = [
        'name', 
        'email', 
        'message', 
        'admin_notes',
        'response'
    ]
    
    date_hierarchy = 'created_at'
    
    ordering = ['-created_at']
    
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'ip_address', 
        'user_agent',
        'responded_at'
    ]
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email')
        }),
        ('Message Details', {
            'fields': ('message', 'priority', 'status')
        }),
        ('Response', {
            'fields': ('response', 'responded_by', 'responded_at'),
            'classes': ('collapse',)
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',),
            'classes': ('collapse',),
            'description': 'Internal notes - not visible to the sender'
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = [
        'mark_as_read',
        'mark_as_replied', 
        'mark_as_archived',
        'set_priority_high',
        'set_priority_medium',
        'set_priority_low'
    ]
    
    # Custom display methods
    def colored_status(self, obj):
        """Display status with color coding"""
        colors = {
            'new': '#ff5722',
            'read': '#2196f3',
            'replied': '#4caf50',
            'archived': '#9e9e9e',
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'
    colored_status.admin_order_field = 'status'
    
    def priority_badge(self, obj):
        """Display priority with badge style"""
        colors = {
            'low': '#4caf50',
            'medium': '#ff9800',
            'high': '#ff5722',
            'urgent': '#e91e63',
        }
        color = colors.get(obj.priority, '#000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display().upper()
        )
    priority_badge.short_description = 'Priority'
    priority_badge.admin_order_field = 'priority'
    
    def short_message_display(self, obj):
        """Display shortened message"""
        return obj.get_short_message(60)
    short_message_display.short_description = 'Message Preview'
    
    def action_buttons(self, obj):
        """Display quick action buttons"""
        if obj.status == 'new':
            return format_html(
                '<span style="color: #ff5722; font-weight: bold;">⚠ NEW</span>'
            )
        elif obj.status == 'replied':
            return format_html(
                '<span style="color: #4caf50;">✓ Replied</span>'
            )
        return format_html('<span style="color: #9e9e9e;">-</span>')
    action_buttons.short_description = 'Quick Status'
    
    # Custom actions
    def mark_as_read(self, request, queryset):
        """Mark selected messages as read"""
        updated = queryset.filter(status='new').update(status='read')
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = '📖 Mark as Read'
    
    def mark_as_replied(self, request, queryset):
        """Mark selected messages as replied"""
        updated = queryset.exclude(status='replied').update(
            status='replied',
            responded_at=timezone.now()
        )
        self.message_user(request, f'{updated} message(s) marked as replied.')
    mark_as_replied.short_description = '✉️ Mark as Replied'
    
    def mark_as_archived(self, request, queryset):
        """Archive selected messages"""
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} message(s) archived.')
    mark_as_archived.short_description = '📦 Archive Messages'
    
    def set_priority_high(self, request, queryset):
        """Set priority to high"""
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} message(s) marked as HIGH priority.')
    set_priority_high.short_description = '🔴 Set Priority: HIGH'
    
    def set_priority_medium(self, request, queryset):
        """Set priority to medium"""
        updated = queryset.update(priority='medium')
        self.message_user(request, f'{updated} message(s) marked as MEDIUM priority.')
    set_priority_medium.short_description = '🟠 Set Priority: MEDIUM'
    
    def set_priority_low(self, request, queryset):
        """Set priority to low"""
        updated = queryset.update(priority='low')
        self.message_user(request, f'{updated} message(s) marked as LOW priority.')
    set_priority_low.short_description = '🟢 Set Priority: LOW'
    
    # Override save to auto-set responded_by
    def save_model(self, request, obj, form, change):
        if change and 'response' in form.changed_data and obj.response:
            if not obj.responded_by:
                obj.responded_by = request.user
            if not obj.responded_at:
                obj.responded_at = timezone.now()
            if obj.status == 'new' or obj.status == 'read':
                obj.status = 'replied'
        super().save_model(request, obj, form, change)


@admin.register(AnonymousDonation)
class AnonymousDonationAdmin(admin.ModelAdmin):
    """Admin interface for anonymous donations"""
    list_display = [
        'get_donor_name',
        'amount',
        'transaction_id',
        'has_receipt',
        'wants_receipt',
        'google_form_submitted',
        'created_at',
    ]
    
    list_filter = [
        'wants_receipt',
        'google_form_submitted',
        'created_at',
        ('created_at', admin.DateFieldListFilter),
    ]
    
    search_fields = [
        'donor_name',
        'donor_email',
        'donor_phone',
        'transaction_id',
        'message',
    ]
    
    readonly_fields = ['created_at', 'ip_address']
    
    fieldsets = (
        ('Donor Information (Optional)', {
            'fields': ('donor_name', 'donor_email', 'donor_phone')
        }),
        ('Donation Details', {
            'fields': ('amount', 'transaction_id', 'message')
        }),
        ('Receipt & Form', {
            'fields': ('receipt', 'wants_receipt', 'google_form_submitted')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def get_donor_name(self, obj):
        """Display donor name or Anonymous"""
        return obj.donor_name if obj.donor_name else 'Anonymous'
    get_donor_name.short_description = 'Donor Name'
    get_donor_name.admin_order_field = 'donor_name'
    
    def has_receipt(self, obj):
        """Display receipt status"""
        return "Yes" if obj.receipt else "No"
    has_receipt.short_description = 'Receipt Uploaded'
    has_receipt.admin_order_field = 'receipt'
