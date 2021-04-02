# Airsoft Shop Website

This is an e-commerce website of airsoft guns and equipment.

![](https://s4.gifyu.com/images/ezgif.com-gif-makerddf3b77a6efc5794.gif)



# Requirements

* Python 3.6+
* Django 3+
* PostgreSQL



# Installation

1. [Install PostgreSQL](https://www.postgresql.org/download/) and create new database.

2. Clone repository.
   
4. Create virtual environment and activate it.

5. Install requirements from the file.

   `pip3 install -r requirements.txt`

   > Note: Ubuntu requires `libpq-dev` and `python-dev` before installation.

6. Fill `.env_sample` with required data and rename the file to `.env`.

7. Make migrations.

8. Run the server `python3 manage.py runserver`.



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