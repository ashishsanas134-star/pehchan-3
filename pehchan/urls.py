from django.urls import path
from . import views

urlpatterns = [
    # Home and Public Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.public_events, name='public_events'),
    path('volunteer-info/', views.public_volunteer, name='public_volunteer'),
    path('donate-info/', views.public_donate, name='public_donate'),
    path('verify-certificate/', views.certificate_verify, name='public_certificate_verify'),
    
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Forgot Password
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
    # Dashboard (Login Required)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard_ui, name='user_dashboard_ui'),
    
    # Events (Login Required)
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/join/', views.join_event, name='join_event'),
    
    # Lifetime Volunteer (Login Required)
    path('volunteer/lifetime/', views.LifetimeVolunteerCreateView.as_view(), name='lifetime_volunteer'),
    
    # Certificates (Login Required)
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('certificates/verify/', views.certificate_verify, name='certificate_verify'),
    path('certificates/donor/', views.donor_certificate_list, name='donor_certificate_list'),
    
    # Donations (Login Required)
    path('donate/material/', views.MaterialDonationCreateView.as_view(), name='material_donation'),
    path('donate/money/', views.MoneyDonationCreateView.as_view(), name='money_donation'),
    
    # Admin Certificate Issuance (Staff Only)
    path('admin/issue-volunteer-certificate/<int:volunteer_id>/', views.issue_volunteer_certificate, name='issue_volunteer_certificate'),
    path('admin/issue-material-donation-certificate/<int:donation_id>/', views.issue_material_donation_certificate, name='issue_material_donation_certificate'),
    path('admin/issue-money-donation-certificate/<int:donation_id>/', views.issue_money_donation_certificate, name='issue_money_donation_certificate'),
]