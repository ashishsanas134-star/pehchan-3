from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import (
    Event, EventVolunteer, LifetimeVolunteer, 
    Certificate, MaterialDonation, MoneyDonation, DonorCertificate, ContactMessage, AnonymousDonation
)
from .forms import (
    SignUpForm, LoginForm, EventVolunteerForm, LifetimeVolunteerForm,
    MaterialDonationForm, MoneyDonationForm, CertificateVerificationForm, ContactMessageForm, AnonymousDonationForm
)

# Add these imports for the forgot password functionality
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string
from .models import PasswordResetOTP
from .forms import ForgotPasswordForm, OTPVerificationForm, ResetPasswordForm


def home(request):
    """Home page view with contact form"""
    print(f"Home view accessed. Method: {request.method}")
    print(f"POST data: {request.POST}")
    
    # Handle contact form submission FIRST (before checking authentication)
    if request.method == 'POST':
        print("Contact form submitted.")
        form = ContactMessageForm(request.POST)
        print(f"Form data: {form.data}")
        print('*****************************************')
        if form.is_valid():
            print("Contact form is valid.")
            # Save the contact message
            contact_message = form.save(commit=False)
            # Optionally capture IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                contact_message.ip_address = x_forwarded_for.split(',')[0]
            else:
                contact_message.ip_address = request.META.get('REMOTE_ADDR')
            # Capture user agent
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            contact_message.save()
            
            # Debug: Print to console
            print(f"Contact message saved: ID={contact_message.id}, Name={contact_message.name}, Email={contact_message.email}")
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('home')
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ContactMessageForm()
    
    # If user is authenticated, redirect to dashboard (for GET requests only)
    if request.user.is_authenticated and request.method == 'GET':
        return redirect('dashboard')
    
    return render(request, 'home.html', {'contact_form': form})


def about(request):
    """About page - accessible to all"""
    return render(request, 'about.html')


def public_events(request):
    """Public events/gallery page - accessible to all"""
    return render(request, 'events.html')


def public_volunteer(request):
    """Public volunteer page - accessible to all"""
    return render(request, 'volunteer.html')


def public_donate(request):
    """Public donate page - accessible to all, handles login/signup and anonymous donations"""
    if request.method == 'POST':
        form_type = request.POST.get('form_type', '')
        
        if form_type == 'signup':
            # Handle signup
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                # Authenticate and login the user
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Registration successful! Welcome to Pehchan.')
                    return redirect('dashboard')
            else:
                # Show error messages
                for field, errors in form.errors.items():
                    if field == '__all__':
                        for error in errors:
                            messages.error(request, f'{error}')
                    else:
                        for error in errors:
                            field_name = field.replace('_', ' ').title()
                            if field == 'password2':
                                field_name = 'Confirm Password'
                            messages.error(request, f'{field_name}: {error}')
        
        elif form_type == 'login':
            # Handle login
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        
        elif form_type == 'anonymous_donation':
            # Handle anonymous donation form submission
            anon_form = AnonymousDonationForm(request.POST, request.FILES)
            if anon_form.is_valid():
                donation = anon_form.save(commit=False)
                # Capture IP address
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    donation.ip_address = x_forwarded_for.split(',')[0]
                else:
                    donation.ip_address = request.META.get('REMOTE_ADDR')
                donation.save()
                messages.success(request, 'Thank you for your anonymous donation! Your contribution has been recorded.')
                return redirect('public_donate')
            else:
                messages.error(request, 'Please fill in the required fields correctly.')
    
    # Create a fresh anonymous donation form for display
    anon_donation_form = AnonymousDonationForm()
    
    return render(request, 'donate.html', {'anon_donation_form': anon_donation_form})


def signup_view(request):
    """User signup view"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Pehchan.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard view"""
    # Get upcoming events
    upcoming_events = Event.objects.filter(status='upcoming').order_by('event_date')
    
    # Get user's joined events
    joined_events = EventVolunteer.objects.filter(user=request.user).select_related('event')
    
    # Get user's certificates
    certificates = Certificate.objects.filter(
        volunteer__user=request.user
    ).select_related('event', 'volunteer')
    
    # Get user's donor certificates
    donor_certificates = DonorCertificate.objects.filter(
        user=request.user
    ).select_related('material_donation', 'money_donation')
    
    # Get user's donations
    material_donations = MaterialDonation.objects.filter(user=request.user)
    money_donations = MoneyDonation.objects.filter(user=request.user)
    
    # Check if user is a lifetime volunteer
    is_lifetime_volunteer = hasattr(request.user, 'lifetime_volunteer')
    
    context = {
        'upcoming_events': upcoming_events,
        'joined_events': joined_events,
        'certificates': certificates,
        'donor_certificates': donor_certificates,
        'material_donations': material_donations,
        'money_donations': money_donations,
        'is_lifetime_volunteer': is_lifetime_volunteer,
    }
    return render(request, 'dashboard.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard view - UI only"""
    return render(request, 'admin_dashboard.html')


@login_required
def user_dashboard_ui(request):
    """User dashboard UI view - UI only"""
    return render(request, 'user_dashboard.html')



class EventListView(LoginRequiredMixin, ListView):
    """List all upcoming events"""
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        return Event.objects.filter(status='upcoming').order_by('event_date')


class EventDetailView(LoginRequiredMixin, DetailView):
    """Event detail view with volunteer join option"""
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if user already joined this event
        context['already_joined'] = EventVolunteer.objects.filter(
            user=self.request.user,
            event=self.object
        ).exists()
        return context


@login_required
def join_event(request, pk):
    """Join an event as a volunteer"""
    event = get_object_or_404(Event, pk=pk)
    
    # Check if user already joined
    if EventVolunteer.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, 'You have already joined this event!')
    else:
        EventVolunteer.objects.create(user=request.user, event=event)
        messages.success(request, f'Successfully joined {event.name} as a volunteer!')
    
    return redirect('event_detail', pk=pk)


class LifetimeVolunteerCreateView(LoginRequiredMixin, CreateView):
    """Become a lifetime volunteer"""
    model = LifetimeVolunteer
    form_class = LifetimeVolunteerForm
    template_name = 'lifetime_volunteer_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        # Check if user is already a lifetime volunteer
        if hasattr(self.request.user, 'lifetime_volunteer'):
            messages.warning(self.request, 'You are already a lifetime volunteer!')
            return redirect('dashboard')
        
        form.instance.user = self.request.user
        messages.success(self.request, 'Congratulations! You are now a lifetime volunteer.')
        return super().form_valid(form)


@login_required
def certificate_list(request):
    """List user's certificates"""
    certificates = Certificate.objects.filter(
        volunteer__user=request.user
    ).select_related('event', 'volunteer')
    
    return render(request, 'certificate_list.html', {'certificates': certificates})


@login_required
def certificate_verify(request):
    """Verify a certificate by ID"""
    certificate = None
    form = CertificateVerificationForm()
    
    if request.method == 'POST':
        form = CertificateVerificationForm(request.POST)
        if form.is_valid():
            cert_id = form.cleaned_data['certificate_id']
            try:
                certificate = Certificate.objects.get(pk=cert_id)
                messages.success(request, 'Certificate found and verified!')
            except Certificate.DoesNotExist:
                messages.error(request, 'Certificate not found. Please check the ID.')
    
    return render(request, 'certificate_verify.html', {
        'form': form,
        'certificate': certificate
    })


@login_required
def donor_certificate_list(request):
    """List user's donor certificates"""
    donor_certificates = DonorCertificate.objects.filter(
        user=request.user
    ).select_related('material_donation', 'money_donation').order_by('-issue_date')
    
    return render(request, 'donor_certificate_list.html', {
        'donor_certificates': donor_certificates
    })


class MaterialDonationCreateView(LoginRequiredMixin, CreateView):
    """Create a material donation"""
    model = MaterialDonation
    form_class = MaterialDonationForm
    template_name = 'material_donation_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Show pickup/courier message
        pickup_msg = self.object.get_pickup_message()
        messages.success(self.request, f'Material donation submitted successfully! {pickup_msg}')
        return response


class MoneyDonationCreateView(LoginRequiredMixin, CreateView):
    """Create a money donation"""
    model = MoneyDonation
    form_class = MoneyDonationForm
    template_name = 'money_donation_form.html'
    success_url = reverse_lazy('dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Static UPI ID for donations
        context['upi_id'] = 'pehchan@upi'  # Replace with your actual UPI ID
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.payment_method = 'upi'
        form.instance.upi_id = 'pehchan@upi'  # Static UPI ID
        messages.success(self.request, 'Money donation submitted successfully! Thank you for your support.')
        return super().form_valid(form)


def forgot_password(request):
    """Handle forgot password request"""
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate a 6-digit OTP
                otp = ''.join(random.choices(string.digits, k=6))
                
                # Set expiration time (10 minutes from now)
                expires_at = timezone.now() + timedelta(minutes=10)
                
                # Save OTP to database
                PasswordResetOTP.objects.create(
                    user=user,
                    otp=otp,
                    expires_at=expires_at
                )
                
                # Send OTP via email
                subject = 'Pehchan - Password Reset OTP'
                message = f"""
                Hello {user.username},
                
                You have requested to reset your password. Please use the following OTP to reset your password:
                
                OTP: {otp}
                
                This OTP is valid for 10 minutes.
                
                If you did not request this, please ignore this email.
                
                Best regards,
                Pehchan Team
                """
                
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                
                # Store user ID in session for later use
                request.session['reset_user_id'] = user.id
                
                messages.success(request, 'An OTP has been sent to your email address.')
                return redirect('verify_otp')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email address.')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot_password.html', {'form': form})


def verify_otp(request):
    """Verify OTP for password reset"""
    if 'reset_user_id' not in request.session:
        messages.error(request, 'Invalid request. Please try again.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            user_id = request.session['reset_user_id']
            
            try:
                user = User.objects.get(id=user_id)
                # Check if OTP exists and is valid
                otp_record = PasswordResetOTP.objects.filter(user=user, otp=otp).first()
                
                if otp_record and otp_record.is_valid():
                    # OTP is valid, remove it from database
                    otp_record.delete()
                    # Store user ID in session for password reset
                    request.session['reset_user_id'] = user.id
                    messages.success(request, 'OTP verified successfully.')
                    return redirect('reset_password')
                else:
                    messages.error(request, 'Invalid or expired OTP. Please try again.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid request. Please try again.')
                return redirect('forgot_password')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'verify_otp.html', {'form': form})


def reset_password(request):
    """Reset password after OTP verification"""
    if 'reset_user_id' not in request.session:
        messages.error(request, 'Invalid request. Please try again.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user_id = request.session['reset_user_id']
            
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                
                # Clear session
                del request.session['reset_user_id']
                
                messages.success(request, 'Your password has been reset successfully. You can now login with your new password.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Invalid request. Please try again.')
                return redirect('forgot_password')
    else:
        form = ResetPasswordForm()
    
    return render(request, 'reset_password.html', {'form': form})
