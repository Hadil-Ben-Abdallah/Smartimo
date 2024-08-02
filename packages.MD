docker compose -f docker-compose.yml up -d

python -m venv venv

venv/Scripts/activate

pip install -U pip

pip install django django-ninja django-extensions psycopg2 
django-tenant-schemas django-tenants

pip install psycopg2

pip install psycopg2-binary

pip install django-environ

pip install django-schema-graph

python -m pip install Pillow

pip freeze > requirements.txt

django-admin startproject `project_name`

python manage.py startapp `app_name`

python manage.py createsuperuser

psql -h localhost -U postgres -d postgres -W # To test the connexion to PostgreSQL database

python manage.py makemigrations

python manage.py shell

from tenants.models import Tenant, Domain

tenant = Tenant(schema_name="public", name="Public")

tenant.save()

domain =  Domain(domain="user.127.0.0.1", tenant=tenant, is_primary=True)

domain.save()

exit()

python manage.py migrate_schemas --shared  # The app delared inside shared_apps will migrate automatically inside public schema

python manage.py migrate_schemas --tenant `schema_name` # while migrating the tenant_apps, we have to give the name of the schema where we want to migrate them

python manage.py migrate_schemas # to migrate all new tables depending on the existing of that table inside which apps in the settings



### After creating schemas, and for th rest of app, we become using : 1) python manage.py makemigrations  2) python manage.py migrate_schemas

