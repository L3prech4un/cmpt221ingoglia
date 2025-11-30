.. _`Development`:

Development
===========
This section is intended for developers that want to create a fix or develop an enhancement to the ``cmpt221ingoglia`` application.

Code of Conduct
---------------
All contributors and maintainers of the software dev 2 project are expected to adhere to the Code of Conduct as outlined.
ex: Coding conventions set by the maintainers are to be followed.

Repository
----------
The repository for software dev 2 is on Github: https://github.com/L3prech4un/cmpt221ingoglia

Development Environment
-----------------------
A `Python virtual environment`_ is recommended. Once the virtual environment is activated, clone the ``cmpt221ingoglia`` repository and prepare the development environment with 

.. _Python virtual environment: https://virtualenv.pypa.io/en/latest/

.. code-block:: text

    $ git clone https://github.com/L3prech4un/cmpt221ingoglia.git
    $ cd cmpt221ingoglia
    $ pip install -r requirements.txt

This will install all local prerequisites needed for ``cmpt221ingoglia`` to run.

Pytest
-------------------
Unit tests are developed using Pytest. To run the test suite, issue:

.. code-block:: text

    $ cd tests
    $ pytest test_app.py

Build Documentation
-------------------
The Github pages site is used to publish documentation for the ``cmpt221ingoglia`` application at l3prech4un.github.io/cmpt221ingoglia/index.html

To build the documentation, issue:

.. code-block:: text
    
    $ cd docs
    $ make html
    # windows users without make installed use:
    $ make.bat html

The top-level document to open with a web-browser will be  ``docs/_build/html/index.html``.

To publish the page, copy the contents of the directory ``docs/_build/html`` into the branch
``gh-pages``. Then, commit and push to ``gh-pages``.