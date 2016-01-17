#!/usr/bin/env bash -e

EXPORT_DIRECTORY=$(mktemp -d -t jrw)

# Export to a local directory
git archive master | tar -x -C $EXPORT_DIRECTORY

# Push up the code
rsync -a $EXPORT_DIRECTORY/ www-data@jokeregistry.online:/www/jokeregistryweb/

ssh www-data@jokeregistry.online << EOF
  cd /www/jokeregistryweb/
  export DJANGO_SETTINGS_MODULE=jokeregistryweb.production
  source bin/activate

  # Install requirements
  pip install -r requirements.txt

  # Collect the static files
  python manage.py collectstatic --noinput

  
EOF

# Collectstatic

# Migrate

# Reload

# Clean up after yourself...
rm -rf $EXPORT_DIRECTORY
