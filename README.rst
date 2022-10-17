|pypi| |actions| |codecov| |downloads|


EFFECT Edc
----------

Fluconazole plus flucytosine vs. fluconazole alone for cryptococcal antigen-positive patients identified through screening:
A phase III randomised controlled trial

The EFFECT Trial

https://www.isrctn.com/ISRCTN30579828

See also https://github.com/clinicedc/edc

|django|

Installation
------------

To setup and run a test server locally

You'll need mysql. Create the database

.. code-block:: bash

  mysql -Bse 'create database effect character set utf8;'


Create a virtualenv, clone the main repo and checkout master

.. code-block:: bash

  conda create -n edc python=3.10
  conda activate edc


Clone the main repo and checkout master

.. code-block:: bash

  mkdir ~/projects
  cd projects
  https://github.com/effect-trial/effect-edc.git
  cd ~/projects/effect-edc
  git checkout main


Copy the test environment file

.. code-block:: bash

  cd ~/projects/effect-edc
  git checkout main
  cp .env.tests .env


Edit the environment file (.env) to include your mysql password in the ``DATABASE_URL``.

.. code-block:: bash

  # look for and update this line
  DATABASE_URL=mysql://user:password@127.0.0.1:3306/effect


Continue with the installation

.. code-block:: bash

  cd ~/projects/effect-edc
  git checkout main
  pip install .
  pip install -U -r requirements.txt
  python manage.py migrate
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


.. |pypi| image:: https://img.shields.io/pypi/v/effect-edc.svg
    :target: https://pypi.python.org/pypi/effect-edc

.. |actions| image:: https://github.com/effect-trial/effect-edc/workflows/build/badge.svg?branch=develop
  :target: https://github.com/effect-trial/effect-edc/actions?query=workflow:build

.. |codecov| image:: https://codecov.io/gh/effect-trial/effect-edc/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/effect-trial/effect-edc

.. |downloads| image:: https://pepy.tech/badge/effect-edc
   :target: https://pepy.tech/project/effect-edc

.. |django| image:: https://www.djangoproject.com/m/img/badges/djangomade124x25.gif
   :target: http://www.djangoproject.com/
   :alt: Made with Django
