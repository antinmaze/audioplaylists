#python manage.py makemigrations
#python manage.py migrate
export ENVIRONMENT="DEV"
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem --keep-meta-shutdown