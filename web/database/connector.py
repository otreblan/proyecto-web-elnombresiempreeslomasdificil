from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
from xdg.BaseDirectory import xdg_data_home
from os.path import join
from pathlib import Path
import json


class Manager:
    Base = declarative_base()
    session = None

    def createEngine(self):
        db_dir = join(xdg_data_home, "web")
        Path(db_dir).mkdir(parents=True, exist_ok=True)

        db_path = 'sqlite:///' + db_dir + '/iChef.db?check_same_thread=False'
        print(db_path)

        engine = create_engine(db_path, echo=False)
        self.Base.metadata.create_all(engine)
        return engine

    def getSession(self, engine):
        if self.session is None:
            Session = sessionmaker(bind=engine)
            session = Session()

        return session


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj)
                          if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None

            return fields

        return json.JSONEncoder.default(self, obj)
