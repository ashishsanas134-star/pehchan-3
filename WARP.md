# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Pehchan is a Django web application for managing NGO operations including events, volunteers, donations, and certificates. The application serves both public visitors and authenticated users, with a comprehensive admin panel for managing all operations.

## Development Commands

### Setup & Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create media directory for file uploads
mkdir -p media
```

### Database Operations

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin superuser
python manage.py createsuperuser
```

### Running the Application

```bash
# Development server
python manage.py runserver

# Access URLs:
# - Main site: http://127.0.0.1:8000/
# - Admin panel: http://127.0.0.1:8000/admin/
```

### Static Files

```bash
# Collect static files (required for production)
python manage.py collectstatic --no-input
```

### Production Build

```bash
# Use the build script for deployment
bash build.sh

# Or manually:
pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### Testing

```bash
# Run Django tests (when test files exist)
python manage.py test

# Run tests for specific app
python manage.py test pehchan

# Run with verbosity
python manage.py test --verbosity=2
```

### Django Shell

```bash
# Interactive Python shell with Django context
python manage.py shell

# Example: Query events
# >>> from pehchan.models import Event
# >>> Event.objects.all()
```

## Architecture Overview

### Application Structure

**Two-tier Django application:**
- `pehchan/` - Main Django app containing all business logic
- `pehchan_webapp/` - Django project settings and configuration

### Data Model Architecture

The application uses **8 core models** with distinct user workflows:

1. **Event Management Flow:**
   - `Event` → `EventVolunteer` → `Certificate`
   - Events have statuses: upcoming, ongoing, completed
   - Volunteers join events and receive certificates upon completion

2. **Volunteer System:**
   - Two volunteer types: Event-specific (`EventVolunteer`) and Lifetime (`LifetimeVolunteer`)
   - Both track approval status (pending/approved)

3. **Donation System:**
   - `MaterialDonation` - Physical items with location-based pickup logic
     - Mumbai: Team pickup
     - Outside Mumbai: Courier to office
   - `MoneyDonation` - UPI-based monetary donations with receipt upload
   - `AnonymousDonation` - Donations without login requirement
   - `DonorCertificate` - Certificates issued for donations

4. **Communication:**
   - `ContactMessage` - Contact form submissions with status tracking and admin response workflow
   - `PasswordResetOTP` - Temporary OTP storage for password reset

### View Architecture Pattern

**Three view patterns used:**
1. **Function-based views** - Authentication, dashboard, simple actions (e.g., `join_event`, `home`)
2. **Class-based views (CBV)** - CRUD operations using Django generic views (`ListView`, `DetailView`, `CreateView`)
3. **Hybrid views** - Public pages that handle both authenticated and anonymous users (e.g., `public_donate`)

**Key architectural pattern:**
- Public pages (home, about, gallery, volunteer-info, donate-info) accessible without login
- Protected pages require `@login_required` decorator or `LoginRequiredMixin`
- Forms use Django's built-in form classes with Bootstrap styling

### URL Routing Structure

```
/ (home) → Public landing page
/about, /gallery, /volunteer-info, /donate-info → Public informational pages
/signup, /login → Authentication
/dashboard → User control panel (login required)
/events → Event browsing and joining (login required)
/certificates → Certificate viewing and verification (login required)
/donate/material, /donate/money → Donation forms (login required)
/admin → Django admin panel
```

### Admin Panel Customization

Heavily customized admin interface using `django-admin-interface`:
- **Custom list displays** with color-coded status badges
- **Bulk actions** for status management (ContactMessage, EventVolunteer)
- **Computed fields** for donation details and certificate numbers
- **Auto-generated certificate numbers** with format: `DON-{YEAR}-{6-digits}`

### Static Files & Media

- **Static files:** Managed by WhiteNoise middleware with compression
  - CSS/JS in `templates/` and `static/`
  - Collected to `staticfiles/` for production
- **Media files:** User uploads (event images, certificates, receipts) stored in `media/`

### Authentication Flow

1. Standard Django auth with custom forms
2. Password reset via OTP (email-based, 10-minute expiry)
3. Session-based user tracking through reset flow
4. Login redirects to dashboard, logout to home

### Template System

- **Base template:** `base.html` - Material Design Lite framework
- **Template inheritance** used throughout
- **Context processors** provide media and auth context globally

## Important Configuration Notes

### Environment Variables

The application reads from environment variables with defaults:
- `SECRET_KEY` - Django secret (has insecure default, must change for production)
- `DEBUG` - Debug mode (default: True)
- `ALLOWED_HOSTS` - Comma-separated hostnames (default: localhost,127.0.0.1)
- `RENDER_EXTERNAL_HOSTNAME` - Auto-added to ALLOWED_HOSTS on Render platform

### Email Configuration

Email is configured for Gmail SMTP (see `settings.py`):
- Used for password reset OTP functionality
- Credentials in settings: `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`
- **Security note:** Email credentials are hardcoded - should use environment variables in production

### UPI Payment Configuration

UPI ID for donations is hardcoded in views:
- Location: `pehchan/views.py`, `MoneyDonationCreateView`
- Lines ~366 and ~372: `'pehchan@upi'`
- **To update:** Search for `pehchan@upi` and replace with actual UPI ID

### Database

- **Development:** SQLite (`db.sqlite3`)
- **Production recommendation:** PostgreSQL or MySQL
- Database included in repo (not typical, but present here)

## Development Patterns & Conventions

### When Modifying Models

1. Always run `makemigrations` after model changes
2. Review generated migration files before applying
3. Run `migrate` to apply changes
4. Update admin.py if new models need admin interface

### When Adding New Views

1. Choose appropriate pattern: function-based vs class-based
2. Add `@login_required` or `LoginRequiredMixin` if authentication needed
3. Create form in `forms.py` if handling user input
4. Add URL pattern to `pehchan/urls.py`
5. Create template in `templates/`
6. Update navigation in `base.html` if needed

### Form Handling Pattern

All forms follow this pattern:
1. Define form in `forms.py` with Bootstrap classes
2. Form validation handled by Django
3. Success messages via `django.contrib.messages`
4. Redirect after successful POST (Post-Redirect-Get pattern)

### Working with Certificates

- Certificate numbers are auto-generated on save (don't override)
- Two certificate types: EventVolunteer and Donor certificates
- File uploads stored in `media/certificates/` and `media/donor_certificates/`

### Material Donation Logic

Location-based pickup message is computed in model:
- Check `MaterialDonation.get_pickup_message()`
- Logic: Mumbai = team pickup, else = courier

## Deployment

Application is configured for Render.com deployment:
- `render.yaml` defines service configuration
- `build.sh` handles build process
- Gunicorn WSGI server for production
- WhiteNoise serves static files in production

## Common Tasks

### Adding a New Event

1. Login to admin panel (/admin/)
2. Go to Events → Add Event
3. Set status as 'upcoming'
4. Users can join via event detail page
5. Update status to 'completed' after event
6. Issue certificates to approved volunteers

### Issuing Certificates

**Volunteer Certificates:**
1. Admin → Certificates → Add Certificate
2. Select event and volunteer
3. Upload certificate file (optional)
4. Certificate ID is auto-generated

**Donor Certificates:**
1. Admin → Donor Certificates → Add Donor Certificate
2. Select user and donation type
3. Link to specific donation (material or money)
4. Certificate number auto-generated with format `DON-{YEAR}-{6-digits}`

### Managing Contact Messages

Admin can:
- View all messages with color-coded status
- Mark as read/replied/archived (bulk actions)
- Set priority levels
- Add internal notes
- Auto-track who responded and when
