# goo

goo is a database wrapper to ease up interaction with your database objects.
It uses sqlalchemy an support the same database types

## Installation

```
pip install goo
```

## Usage

Database connection is initiated when you import the package `import goo`.
It will lock for a connection string (http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) in the environment variable `GOO_URL` or for a `.goo` file in your current directory.
You can also specify a custom goo file using the environment variable `GOO_FILE`.
The environment variable `GOO_ECHO` allow you to enable sqlalchemy debug echo mode.

### Object definition

Object are defined by inheriting `goo.Base` class, it then uses the same syntax as sqlalchemy.

```
from goo import Base, utcnow
from sqlalchemy import Column, String, Integer, DateTime

class User(Base):
    __tablename__ = 'user'

    name = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    age = Column(Integer, nullable=True, default='1')
```

### Database migration

You can run your sqlalchemy create_all using goo

```
# import all your objects definitions
from user import User
from goo import create_all

# Create your tables
create_all()

# Drop your tables
drop_all()
```

### Create an object

Considering you have your `User` class and done the `create_all()`

```
from user import User

# create the object
my_user = User.create(name='John', age=42)

# commit it
my_user.commit()
```

### Get an object

Considering you have your `User` class, done the `create_all()` and created your first object

```
from user import User

# By id
my_user = User.get(id='C88B8570-53BA-4051-B198-F47981D2D299')
if my_user is None:
    raise Exception('Could not retrieve User')

# With filter
my_user = User.get(filter=[User.name='John'])
if my_user is None:
    raise Exception('Could not retrieve User')

# With filter_by
my_user = User.get(filter_by={'name': 'John'})
if my_user is None:
    raise Exception('Could not retrieve User')
```

### List objects

Considering you have your `User` class, done the `create_all()` and created several objects

```
from user import User

# retrieve all users
user_list = User.list()
if not user_list:
    raise Exception('No User in database')

# With filter
user_list = User.list(filter=[User.age.in_(42, 18, 36)])
if not user_list:
    raise Exception('No Users found')

# With filter_by
user_list = User.list(filter_by={'age': 42})
if not user_list:
    raise Exception('No Users found')
```

### Update an object

Considering you have your `User` class, done the `create_all()` and created an object

```
from user import User

# By id
my_user = User.get(id='C88B8570-53BA-4051-B198-F47981D2D299')
if my_user is None:
    raise Exception('Could not retrieve User')

my_user.update(age=57)
my_user.commit()
```

### Delete an object

Considering you have your `User` class, done the `create_all()` and created an object

```
from user import User

# By id
my_user = User.get(id='C88B8570-53BA-4051-B198-F47981D2D299')
if my_user is None:
    raise Exception('Could not retrieve User')

user_dict = my_user.delete()
print('User was %s' % user_dict['name'])
```

## Development

(Commands are executed in project root)

I recommend using python 3.6, using pyenv (https://github.com/pyenv/pyenv):

```
$ make pyenv
```

Setup your virtualenv

```
$ make venv
$ source venv/bin/activate
```

Install requirements

```
$ make requirements
```

Setup your configuration, see

```
$ vim .goo
$ export GOO_ECHO=1
```

Run pep8

```
make pep8
```

Run tests

```
$ make tests
```
