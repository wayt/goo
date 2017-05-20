from goo.base import Base, session
from sqlalchemy import create_engine
from goo.time import utcnow
from pathlib import Path
import os

__all__ = ['init', 'create_all', 'drop_all', 'Base', 'session', 'utcnow']

DEFAULT_GOO_FILE = '.goo'


def init(url: str, echo: bool = False):
    """sqlalchemy engine initialization

    :param url: sqlalchemy create_engine url param,
      see http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls

    :param echo: enable sqlalchemy engine echo mode
      see http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine.params.echo
    """
    engine = create_engine(name_or_url=url)
    engine.echo = echo
    Base.metadata.bind = engine
    session.configure(bind=engine)


def create_all():
    Base.metadata.create_all()


def drop_all():
    session.close()
    Base.metadata.drop_all()


echo = (os.environ.get('GOO_ECHO', '0') == '1')

if 'GOO_URL' in os.environ:
    init(url=os.environ.get('GOO_URL'),
         echo=echo)
else:
    goo_file = Path(os.environ.get('GOO_FILE', DEFAULT_GOO_FILE))
    if goo_file.is_file():
        with goo_file.open('r') as f:
            url = f.read().strip()
            init(url=url, echo=echo)
