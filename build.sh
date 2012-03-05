mkdir sqlite3
cd pml
make
cd ..
cd django_magpie
python manage.py collectstatic
python manage.py syncdb
cd ..
chown -R 775 sqlite3
chown -R 755 resources
