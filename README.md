# TimeTable Manager

Timetable manager will help you to assign a teacher for a class
if the designated teacher is not available.


### Pre-requirements
   * [Python 3.6+](https://www.python.org/downloads/)

### Setting up
* clone the repo
* Setup virtual environment
    * virtualenv venv -p python3
    * source venv/bin/activate
* pip install requirements.txt 

### Execute the program
    python manage.py runserver
 
### Testing
    python manage.py test


###APIs

#####Teachers
    /api/v0/teachers
* To list all teachers of a school with code school_code

    ```/?school__code=school_code```
* Filter teachers while searching by name

    ```/?school__code=school_code&first_name__contains=asd```
