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
* pip install -r requirements.txt 

### Execute the program
    python manage.py runserver
 
### Testing
    python manage.py test


### APIs

##### Teachers
    /api/v0/teachers
* To list all teachers of a school with code school_code

    ```/?school__code=school_code```
* Filter teachers while searching by name

    ```/?school__code=school_code&first_name__contains=asd```


##### Periods
    /api/v0/periods
* To list time table for a class

    ```/?admission=year&classroom=classroom_id```

* To list time table for a class of a day

    ```/?admission=year&classroom=classroom_id&weekday=1```
        
        1 for Monday
        6 for Saturday

    ```/?admission=year&classroom=classroom_id&date=2019-12-20```

* To list schedule of a teacher on a particular day

    ```/?admission=year&date=2019-12-20&teacher=teacher_id```
 
* To list available teachers for replacement for a particular period, period_id
    
    ```/period_id/free-teachers/?date=Y-m-d```

        Date is a mandatory argument for this api
        Date is used to filter out the teachers who has an extra period adjustment on same day same period.

* To list insights regarding period adjustment of period_id with teacher_id

    ```/period_id/insights/?teacher_id=teacher_id&date=Y-m-d```


##### Period Adjustment
    /api/v0/period-adjustments

* List all period adjustments of a day

    ```/?date=Y-m-d```
