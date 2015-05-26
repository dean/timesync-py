# Timesync

This is an application written using [Flask](flask.pocoo.org) to submit and 
coordinate time entries for work done on application or projects within an 
organization.

We also use [SQLAlchemy](http://docs.sqlalchemy.org/en/rel_0_9/)
 to interact with the database.

## Installation

Run the following commands.

```sh
git clone https://github.com/dean/timesync-py
cd timeysnc-py
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

If you run into issues running ```pip install -r requirements.txt``` make sure
you have python header files such as ```python-dev``` and ```python-mysqldb``` 
on debian based systems or the equivalent. 

To setup the database run:
```sh
python manage.py setup_db
```

## Usage

Be sure to in your virtual environment before running any commands!
```sh
source env/bin/activate
```

Once that's done, run
```
python manage.py runserver
```

and you should notice that the server is running on ```localhost:3000```.

## Support

Please [open an issue](https://github.com/dean/timesync-py/issues/new) for questions and concerns.

## Contributing

Fork the project, commit your changes, and [open a pull request](https://github.com/dean/timesync-py/compare/).
