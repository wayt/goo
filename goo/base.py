from typing import Dict, List
from sqlalchemy import Column, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from uuid import uuid4

session = scoped_session(sessionmaker())
_model = declarative_base()


def str_uuid4() -> str:
    """return an uuid4 as a string"""
    return str(uuid4())


class Base(_model):

    """Base class for database object"""

    __abstract__ = True

    query = session.query_property()

    # id can be override during inheritence
    id = Column(UUID(as_uuid=False), primary_key=True, default=str_uuid4)

    def to_dict(self) -> Dict[str, any]:
        """Serialize an object to a dict"""

        # When committed, an ORM object is expired, which means that
        # obj.__dict__ does not return its properties.
        # session.refresh reloads the object from database
        # http://docs.sqlalchemy.org/en/latest/orm/
        # session_state_management.html#refreshing-expiring
        state = inspect(self)
        if state.expired and state._attached:
            session().refresh(self)

        d = dict(self.__dict__)

        # Remove SQLAlchemy stuff
        try:
            del d['_sa_instance_state']
        except KeyError:
            pass

        return d

    @classmethod
    def create(cls, **kwargs) -> object:
        """Create a new object using kwargs as attributes

        This method can be override during inheritence,
        ensure to call :meth:`._create` to create the actual object.

        You MUST call :meth:`.commit` to actually commit object
        to database.
        """
        return cls._create(**kwargs)

    @classmethod
    def _create(cls, **kwargs) -> object:
        """Internal create a new object using kwargs as attributes

        This method should not be override as it contains the
        database logic.

        You MUST call :meth:`.commit` to actually commit object
        to database.
        """
        obj = cls(**kwargs)
        session.add(obj)
        return obj

    def commit(self) -> object:
        """Commit an object to database"""
        session.commit()
        return self

    @classmethod
    def get(cls, id: any=None, filter: List[any]=None,
            filter_by: Dict[str, any]=None) -> object:
        """Get a single object from database

        This method can be override during inheritence,
        ensure to call :meth:`._get` to do the actual query.

        Only one of :param:`id` :param:`filter` :param:`filter_by`
        is required.

        :param id: object id, depend on :attr:`.id` type

        :param filter: sqlalchemy :meth:`sqlalchemy.orm.query.Query.filter` parameter

        :param filter_by: :meth:`sqlalchemy.orm.query.Query.filter_by` parameter
        """
        obj = cls._get(id=id, filter=filter, filter_by=filter_by)
        return obj

    @classmethod
    def _get(cls, id: any=None, filter: List[any]=None,
             filter_by: Dict[str, any]=None) -> object:
        """Internal get a single object from database

        This method should not be override as it contains the
        database logic.

        Only one of :param:`id` :param:`filter` :param:`filter_by`
        is required.

        :param id: object id, depend on :attr:`.id` type

        :param filter: sqlalchemy :meth:`sqlalchemy.orm.query.Query.filter` parameter

        :param filter_by: :meth:`sqlalchemy.orm.query.Query.filter_by` parameter
        """

        query = cls.query

        if id:
            query = query.filter_by(id=id)
        elif filter:
            query = query.filter(*filter)
        elif filter_by:
            query = query.filter_by(**filter_by)
        obj = query.first()

        return obj

    @classmethod
    def list(cls, filter: List[any]=None, filter_by: Dict[str, any]=None,
             order_by: str=None, order: str='ASC',
             limit: int=None) -> List[object]:
        """Get multiple objects from database

        This method can be override during inheritence,
        ensure to call :meth:`._list` to do the actual query.

        Only one of :param:`filter` :param:`filter_by`
        is required.

        :param filter: sqlalchemy :meth:`sqlalchemy.orm.query.Query.filter` parameter

        :param filter_by: :meth:`sqlalchemy.orm.query.Query.filter_by` parameter

        :param order_by: sql ``ORDER BY`` field

        :param order: sql ordering, ``ASC`` or ``DESC``

        :param limit: object count limit, sql ``LIMIT`` keyword
        """
        objs = cls._list(filter=filter, filter_by=filter_by,
                         order_by=order_by, order=order,
                         limit=limit)
        return objs

    @classmethod
    def _list(cls, filter: List[any]=None, filter_by: Dict[str, any]=None,
              order_by: str=None, order: str='ASC',
              limit: int=None) -> List[object]:
        """Internal get multiple objects from database

        This method should not be override as it contains the
        database logic.

        Only one of :param:`filter` :param:`filter_by`
        is required.

        :param filter: sqlalchemy :meth:`sqlalchemy.orm.query.Query.filter` parameter

        :param filter_by: :meth:`sqlalchemy.orm.query.Query.filter_by` parameter

        :param order_by: sql ``ORDER BY`` field

        :param order: sql ordering, ``ASC`` or ``DESC``

        :param limit: object count limit, sql ``LIMIT`` keyword
        """
        if order_by:
            order_attribute = getattr(cls, order_by)
        else:
            order_attribute = cls.id
        query = cls.query

        if filter_by:
            query = query.filter_by(**filter_by)
        elif filter:
            query = query.filter(*filter)

        query = query.order_by(
                order_attribute.desc() if order.upper() == 'DESC' else order_attribute)
        if limit:
            query = query.limit(limit)
        return query.all()

    def update(self, **kwargs) -> object:
        """Update an object using kwargs as attributes

        You MUST call :meth:`.commit` to actually commit object
        to database.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def delete(self) -> Dict[str, any]:
        """Delete an object from database

        This method does not require to call :meth:`.commit`.
        """
        obj_dict = self.to_dict()
        session.delete(self)
        self.commit()
        return obj_dict
