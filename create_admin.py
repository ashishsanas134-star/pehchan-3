import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pehchan_webapp.settings')

# Initialize Django
django.setup()

from django.contrib.auth.models import User

def create_admin():
    # Fetch credentials from environment variables with fallbacks
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin')

    # Check if the user already exists
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}...")
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("Superuser created successfully!")
    else:
        print(f"Superuser '{username}' already exists. Skipping creation.")

if __name__ == "__main__":
    try:
        create_admin()
    except Exception as e:
        print(f"Error creating superuser: {e}")
