#!/usr/bin/env bash -e

if [ `git rev-parse --abbrev-ref HEAD` != "master" ]; then
	echo "You should only deploy on master!"
	exit 1
fi

EXPORT_DIRECTORY=$(mktemp -d -t jrw)

# Export to a local directory
git archive HEAD | tar -x -C $EXPORT_DIRECTORY

# Push up the code
rsync -a $EXPORT_DIRECTORY/ www-data@jokeregistry.online:/www/jokeregistryweb/

ssh -q www-data@jokeregistry.online << EOF
  cd /www/jokeregistryweb/
  export DJANGO_SETTINGS_MODULE=jokeregistryweb.production
  source bin/activate

  # Install requirements
  pip install -r requirements.txt

  # Collect the static files
  python manage.py collectstatic --noinput

  # Run DB migrations
  python manage.py migrate --noinput

  # Reload the web server
  touch /etc/uwsgi-emperor/vassals/jokeregistryweb.ini
EOF

# We need to re-run this every 90 days to get new certs...
# ./letsencrypt-auto certonly --webroot -w /www/jokeregistryweb/public/ -d www.jokeregistry.online -d jokeregistry.online

# Clean up after yourself...
rm -rf $EXPORT_DIRECTORY