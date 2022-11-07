<h1 align="center">Airsoft Shop Website</h1>

<p align="center">This is an e-commerce website of airsoft guns and equipment.</p>

<p align="center">
   <img alt="hi" src="" align="center"/>
</p>



# Requirements

* Python 3.6+
* Django 3+
* PostgreSQL



# Installation

1. [Install PostgreSQL](https://www.postgresql.org/download/) and create new database.

2. Clone the repository.
   
4. Create virtual environment and activate it.

5. Install requirements from the file.

   `pip install -r requirements.txt`

   > Note: Ubuntu requires `libpq-dev`, `python-dev` and `build-essential` before installation.

6. Fill `env_sample` with required data and rename it `.env`.

7. Make migrations and migrate.

   You can do it mannualy or use a script `scripts/migrations.sh`.

8. Create superuser by running a script `scripts/createsuperuser.py`.

9. Run the server `python manage.py runserver`.



# Implemented

* Products
* Product Categories (tree structure)
* Cart
* Cart for Anonymous User (using Cookie)
* Customer
* Registration
* Email confirmation of registration
* Edit profile
* Order procedure 
