# Pehchan - Empowering Communities

A comprehensive Django web application for managing NGO events, volunteers, donations, and certificates.

## Features

### 1. Admin Features
- Built-in Django admin panel for managing all resources
- Create, edit, and delete events
- View and manage volunteers (event-specific and lifetime)
- Track donations (material and monetary)
- Issue certificates to volunteers

### 2. User Authentication
- User registration and login system
- Personalized dashboard for each user
- Secure authentication using Django's built-in system

### 3. Event Management
- Browse upcoming events
- View detailed event information
- Join events as a volunteer
- Track event status (upcoming, ongoing, completed)

### 4. Volunteer System
- Join individual events as a volunteer
- Become a lifetime volunteer
- Track volunteer status (pending/approved)
- View volunteer history

### 5. Certificate System
- Admins can issue certificates to volunteers
- Users can view all their certificates
- Certificate verification by ID
- Download certificates

### 6. Donation System
- **Material Donations**: Donate items with automatic pickup/courier logic
  - Mumbai: Team pickup
  - Outside Mumbai: Courier to office
- **Money Donations**: UPI-based donations with receipt upload
- View donation history

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Development Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and set your values (at minimum SECRET_KEY)
   # For local development, you can set DEBUG=True
   ```

4. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

6. **Create media directory**:
   ```bash
   mkdir media
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Admins
1. Login to the admin panel at `/admin/`
2. Create events with details (name, date, location, description, image)
3. View and manage volunteer applications
4. Issue certificates to volunteers after event completion
5. Track all donations

### For Users
1. Sign up for a new account
2. Login and access your dashboard
3. Browse and join upcoming events
4. Apply to become a lifetime volunteer
5. Make material or money donations
6. View and download your certificates
7. Verify certificates by ID

## Project Structure

```
pehchan-webapp/
├── pehchan/                    # Main Django app
│   ├── models.py               # Database models
│   ├── views.py                # View logic
│   ├── forms.py                # Form definitions
│   ├── admin.py                # Admin configurations
│   └── urls.py                 # App URL patterns
├── pehchan_webapp/             # Project settings
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI configuration
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── home.html               # Homepage
│   ├── signup.html             # User registration
│   ├── login.html              # User login
│   ├── dashboard.html          # User dashboard
│   ├── event_list.html         # Event listing
│   ├── event_detail.html       # Event details
│   ├── certificate_list.html   # User certificates
│   ├── certificate_verify.html # Certificate verification
│   ├── material_donation_form.html
│   ├── money_donation_form.html
│   └── lifetime_volunteer_form.html
├── media/                      # Uploaded files (created on setup)
├── manage.py                   # Django management script
└── requirements.txt            # Python dependencies
```

## Models

### Event
- Event information (name, description, date, location)
- Event image
- Status (upcoming, ongoing, completed)

### EventVolunteer
- Links users to events they've joined
- Tracks volunteer status (pending/approved)

### LifetimeVolunteer
- One-time registration as a lifetime volunteer
- Stores motivation statement

### Certificate
- Links volunteers to events they've completed
- Certificate file storage
- Unique certificate ID for verification

### MaterialDonation
- Item donation tracking
- Location-based pickup/courier logic
- Donation status tracking

### MoneyDonation
- Monetary donation tracking
- UPI payment integration
- Receipt upload functionality

## Customization

### Update UPI ID
In `pehchan/views.py`, find the `MoneyDonationCreateView` class and update:
```python
context['upi_id'] = 'your-upi-id@upi'  # Line ~220
form.instance.upi_id = 'your-upi-id@upi'  # Line ~225
```

### Styling
The project uses Material Design Lite for styling. You can customize the appearance by:
- Modifying the styles in `templates/base.html`
- Adding custom CSS files in the templates directory
- Changing Material Design Lite themes

## Production Deployment

### Deploying to Render

This project is configured for easy deployment on [Render](https://render.com/).

1. **Push your code to GitHub**

2. **Connect to Render**:
   - Go to Render Dashboard → New Web Service
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Configure Environment Variables**:
   The following variables will be set automatically:
   - `DATABASE_URL` - PostgreSQL database connection
   - `SECRET_KEY` - Auto-generated secure key
   - `DEBUG` - Set to `false`
   
   You need to manually set:
   - `EMAIL_HOST_USER` - Your email address
   - `EMAIL_HOST_PASSWORD` - Your email app password
   - `ALLOWED_HOSTS` - Your domain name (optional, Render adds it automatically)

4. **Deploy** - Render will handle the rest!

### Production Checklist

Before deploying to production, ensure:

- ✅ `SECRET_KEY` is set via environment variable (not hardcoded)
- ✅ `DEBUG=False` in production
- ✅ `ALLOWED_HOSTS` is configured with your domain
- ✅ PostgreSQL database is configured
- ✅ Email credentials are set (if using email features)
- ✅ HTTPS is enabled (Render provides this automatically)
- ✅ Static files are collected (`collectstatic` runs automatically)
- ✅ Media files storage is configured for production (consider using AWS S3 or similar)

### Security Features Enabled

The project now includes production-ready security:

- 🔒 HTTPS redirect (automatic in production)
- 🔒 HTTP Strict Transport Security (HSTS)
- 🔒 Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- 🔒 XSS protection headers
- 🔒 Content type sniffing protection
- 🔒 Session security (HTTPOnly cookies, 1-hour expiry)
- 🔒 CSRF protection with SameSite cookies
- 🔒 Comprehensive error logging

## Security Notes

✅ **This project is now production-ready!**

All critical security issues have been addressed:
1. ✅ `SECRET_KEY` must be set via environment variable (no hardcoded fallback)
2. ✅ `DEBUG` defaults to `False` for production safety
3. ✅ `ALLOWED_HOSTS` properly configured
4. ✅ Production security headers enabled (HTTPS, HSTS, XSS protection)
5. ✅ Secure session and CSRF cookie settings
6. ✅ Email credentials removed from code (must use environment variables)
7. ✅ Comprehensive error logging configured

For local development, create a `.env` file from `.env.example` and set `DEBUG=True`.

## Contributing

This is a project for the Pehchan NGO. For contributions or issues, please contact the project maintainers.

## License

Copyright © 2025 Pehchan - Empowering Communities. All rights reserved.

## Support

For support or questions, contact: madad@pehchanyui.in
