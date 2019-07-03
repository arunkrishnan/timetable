# TimeTable Manager

Timetable manager will help you to assign a teacher for a class
if the designated teacher is not available.


### Pre-requirements
   * [Python 3.6+](https://www.python.org/downloads/)
   * [pipenv](https://docs.pipenv.org/en/latest/)

### Setting up
* clone the repo
* cd timetable
* pipenv install

### Execute the program
    pipenv run ./manage.py runserver
 
### Testing
    pipenv run python manage.py test

### Load data
    pipenv run ./manage.py loaddata schools/fixtures/cms.json
    pipenv run ./manage.py loaddata classrooms/fixtures/cms.json

### APIs

All APIs are paginated

##### Teachers
    /api/v0/teachers
* To list all teachers of a school

* Filter teachers while searching by name

    ```/?first_name__contains=asd```


##### Periods
    /api/v0/periods
* To list time table for a class

    ```/?classroom=classroom_id```

* To list time table for a class of a day

    ```/?classroom=classroom_id&weekday=1```
        
        1 for Monday
        6 for Saturday

    ```/?classroom=classroom_id&date=2019-12-20```

* To list schedule of a teacher on a particular day

    ```/?date=2019-12-20&teacher=teacher_id```
 
* To list available teachers for replacement for a particular period, period_id
    
    ```/period_id/free-teachers/?date=Y-m-d```

        Date is a mandatory argument for this api
        Date is used to filter out the teachers who has an extra period adjustment on same day same period.

* To list insights regarding period adjustment of period_id with subject_teacher_id

    ```/period_id/insights/?tsubject_eacher_id=subject_teacher_id&date=Y-m-d```


##### Period Adjustment
    /api/v0/period-adjustments

* List all period adjustments of a day

    ```/?date=Y-m-d```

* Add a new adjustment

    ``` POST /api/v0/period-adjustments```
    with payload

    ```
        {
            "adjusted_date": "2019-12-31",
            "period": 1,
            "adjusted_by": 22
        }

    ```


##### APIs are limited to single school for now, and eliminated need for login