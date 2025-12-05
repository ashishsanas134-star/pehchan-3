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

### Installation

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

3. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

5. **Create media directory**:
   ```bash
   mkdir media
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
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

## Security Notes

⚠️ **Important for Production**:
1. Change the `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False` in `settings.py`
3. Configure `ALLOWED_HOSTS` properly
4. Use a production database (PostgreSQL, MySQL)
5. Set up proper static file serving
6. Use HTTPS
7. Configure email backend for notifications

## Contributing

This is a project for the Pehchan NGO. For contributions or issues, please contact the project maintainers.

## License

Copyright © 2025 Pehchan - Empowering Communities. All rights reserved.

## Support

For support or questions, contact: madad@pehchanyui.in
