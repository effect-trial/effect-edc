|pypi| |actions| |codecov| |downloads| |clinicedc|


EFFECT Edc
----------

|effect_logo|

The EFFECT Trial

Fluconazole plus flucytosine vs. fluconazole alone for cryptococcal antigen-positive patients identified through screening:
A phase III randomised controlled trial

(EFFECT - Efficacy of Flucytosine and Fluconazole as Early Cryptococcal Treatment)

https://www.isrctn.com/ISRCTN30579828

See also https://github.com/clinicedc/edc

|django|

Installation
------------

To setup and run a test server locally

You'll need mysql. Create the database

.. code-block:: bash

  mysql -Bse 'create database effect character set utf8;'


Clone the main repo and checkout main

.. code-block:: bash

  mkdir ~/projects
  cd projects
  https://github.com/effect-trial/effect-edc.git
  cd ~/projects/effect-edc
  git checkout main


Create a venv with uv

.. code-block:: bash

    uv venv
    source .venv/bin/activate
    uv sync --no-sources --upgrade

Copy the test environment file

.. code-block:: bash

  mkdir ~/.clinicedc/effect_edc
  cd ~/projects/effect-edc
  cp .env.tests ~/.clinicedc/effect_edc/.env


Edit the environment file (.env) to include your mysql password in the ``DATABASE_URL``.

.. code-block:: bash

  # look for and update this line
  DATABASE_URL=mysql://user:password@127.0.0.1:3306/effect


Continue with the installation. FOr this example we setup up a test server (DEBUG=True)

.. code-block:: bash

  cd ~/projects/effect-edc
  python manage.py migrate --settings=effect_edc.settings.debug
  python manage.py import_randomization_list
  python manage.py import_holidays


Create a user and start up `runserver`

.. code-block:: bash

  cd ~/projects/effect-edc
  git checkout main
  python manage.py createsuperuser
  python manage.py runserver


Login::

  http://localhost:8000

.. |effect_logo| image:: https://github.com/effect-trial/effect-edc/blob/develop/docs/effect_logo_sm.jpg
   :target: https://github.com/effect-trial/effect-edc

.. |pypi| image:: https://img.shields.io/pypi/v/effect-edc.svg
   :target: https://pypi.python.org/pypi/effect-edc

.. |actions| image:: https://github.com/effect-trial/effect-edc/actions/workflows/build.yml/badge.svg
   :target: https://github.com/effect-trial/effect-edc/actions/workflows/build.yml

.. |codecov| image:: https://codecov.io/gh/effect-trial/effect-edc/branch/develop/graph/badge.svg
   :target: https://codecov.io/gh/effect-trial/effect-edc

.. |downloads| image:: https://pepy.tech/badge/effect-edc
   :target: https://pepy.tech/project/effect-edc

.. |django| image:: https://www.djangoproject.com/m/img/badges/djangomade124x25.gif
   :target: http://www.djangoproject.com/
   :alt: Made with Django

.. |clinicedc| image:: https://img.shields.io/badge/framework-Clinic_EDC-green
   :alt:Made with clinicedc
   :target: https://github.com/clinicedc
