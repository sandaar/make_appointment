#!/bin/bash

echo "Running start.sh"

echo "Updating repositories"
sudo apt-get update

echo "Installing python3, pip"
sudo apt-get install python3 python3-pip -y

echo "Installing required packages"
sudo pip3 install -r requirements.txt

echo "Migrating DB"
cd make_appointment
python3 manage.py makemigrations
python3 manage.py migrate

echo "Loading fixtures"
python3 manage.py loaddata data.xml

echo "Creating django superuser"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python3 manage.py shell

echo "Running app on 0.0.0.0:80"
sudo python3 manage.py runserver 0.0.0.0:80
