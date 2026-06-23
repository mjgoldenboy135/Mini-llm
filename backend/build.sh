#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Create a superuser non-interactively if env vars are set
if [ -n "$DJANGO_SUPERUSER_MOBILE" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py shell -c "
from accounts.models import User
if not User.objects.filter(mobile='$DJANGO_SUPERUSER_MOBILE').exists():
    User.objects.create_superuser(
        mobile='$DJANGO_SUPERUSER_MOBILE',
        name='Admin',
        password='$DJANGO_SUPERUSER_PASSWORD',
    )
    print('Superuser created.')
else:
    print('Superuser already exists.')
"
fi
