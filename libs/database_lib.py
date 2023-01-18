import sqlalchemy as sq
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------------------------- #
#                            Connection to database                            #
# ---------------------------------------------------------------------------- #

class Database():
    # Se crea conexión a base de datos
    def __init__(self, 
        controller, user, password, nm_database, schema, host, port) -> None:
        try:
            self.controller = controller
            self.user = user
            self.password = password
            self.database = nm_database
            self.schema = schema
            self.host = host
            self.port = port
            url_engine = '{}://{}:{}@{}:{}/{}'.format(
                self.controller, self.user, self.password, self.host, self.port, self.database)
            self.engine = sq.create_engine(url_engine, connect_args=(
                {'options': "-csearch_path={}".format(self.schema)}
                if self.schema != False else {}
            ))
            self.session = Session(self.engine)
            self.sessionmaker = sessionmaker(bind=self.engine)()
        except Exception as e:
            print("SQLAlquemy {} tuvo un error: {}".format(
                sq.__version__, e))
