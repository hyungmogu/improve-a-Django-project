# THPWD09 - Improve a Django Project

This is the ninth project to team tree house's Python Web Tech Degree.

## Goal
- Troubleshoot a third-party project given by team treehouse, and ensure that it is optimized and is running without errors

## Deliverables / Objectives

1. Database queries
    - No view has more than 5 queries. Queries must take less than 100ms combined

2. Template inheritance
    - Templates inherit nicely to reduce the total amount of code written.

3. Model fields
    - Model fields are corrected to store correct value types. Migrations are included to change the field types.

4. Form validation
    - Form validation is corrected for proper use of clean(), clean_field(), and validators.

5. Testing
    - Test coverage is at or above 75%.

6. Python Code Style
    - The code is clean, readable, and well organized. It complies with most common PEP 8 standards of style.


## Steps to running testing program
1. Once in project root folder of virtual environment (`step 3` under Steps to Running/Exiting the Program), type `coverage run --source='.' manage.py test menu` to setup info about the % of code covered
2. In project root folder, type `python manage.py test` to run the testing program
3. In project root folder, type `coverage report` to see the result

## Steps to Running/Exiting the Program
1. Install pipenv by typing `pip install pipenv` or `pip3 install pipenv` for python3 users
2. In project root folder, install dependencies by typing `pipenv install`
3. In project root folder, enter virtual environment by typing `pipenv shell`
4. In `improve_django` of project root folder, run `python manage.py makemigrations menu`
5. In `improve_django` of project root folder, run `python manage.py migrate`
6. In `improve_django` of project root folder, run by typing `python manage.py runserver`
7. Open chrome and enter given url (i.e. `http://127.0.0.1:8000/`)
8. Once done, exit django by pressing `Ctrl`+`C` and virtual environment by typing `exit`