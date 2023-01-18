import datetime
import json
import sys
import dotenv
from libs.database_lib import Database


class BaseController():
    values_allow = []
    def __init__(self) -> None:
        self.env = dotenv.dotenv_values(f".env")
        self.db = Database(
            self.env['DB_CONTROLLER'],
            self.env['DB_USER'],
            self.env['DB_PASSWORD'],
            self.env['DB_NAME'],
            False,
            self.env['DB_HOST'],
            self.env['DB_PORT']
        )

    # Seleccionar todos los registros filtrados
    def select(self, filters = None):
        try:
            query_filters = []
            if filters:
                for filter in filters:
                    if filter in self.model.as_array():
                        query_filters.append(
                            self.model_concept.__table__.columns.get(
                                filter
                            ) == (filters)[filter]
                        )

                    else:
                        return json.dumps({"error": f"Fail. not filter allow {filter}"})
                
            consult = self.db.sessionmaker.query(
                self.model_concept
            ).filter(*query_filters)
            result = []
            for value in (consult.all()):
                result.append(value.as_dict())
                
            return json.dumps({"data": result if len(result) else None})

        except Exception as e:
            print(' \n Error on line {}'.format(
                sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return json.dumps({"error": str(e.args)})

    # Seleccionar último registro filtrado
    def select_last(self, filters):
        try:
            query_filters = []
            for filter in filters:
                if filter in self.model.as_array():
                    query_filters.append(
                        self.model_concept.__table__.columns.get(
                            filter
                        ) == (filters)[filter]
                    )

                else:
                    return json.dumps({"error": f"Fail. not filter allow {filter}"})
            consult = self.db.sessionmaker.query(
                self.model_concept
            ).filter(*query_filters)
            result_one = consult.order_by(
                self.model_concept.date_created.desc()).first()
            return json.dumps({"data": result_one.as_dict() if result_one else None})

        except Exception as e:
            print(' \n Error on line {}'.format(
                sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return json.dumps({"error": str(e.args)})

    # Guardar registro
    def save(self, request):
        try:
            # Validar valores recibidos en el Request
            validate_values = self.validate_values(request)
            if validate_values != False:
                return validate_values

            setattr(self.model, "date_created",
                    str(datetime.datetime.now()))

            for value_allow in self.values_allow:
                if value_allow in request:
                    setattr(self.model, value_allow,
                            request[value_allow])
            self.db.session.add(self.model)
            self.db.session.flush()
            self.db.session.commit()

            return json.dumps({"message": "Created", "data": self.model.as_dict()})

        except Exception as e:

            print(' \n Error on line {}'.format(
                sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return json.dumps({"error": str(e.args)})
    
    # Eliminar en cascada
    def delete_cascade(self, request):
        try:
            element_query = self.db.session.query(
                self.model_concept
            ).filter_by(id=request['id']).first()
            consult = self.db.session.delete(element_query)
            print(consult)
            self.db.session.commit()
            return json.dumps({"message": "Deleted", "data": self.model.as_dict()})
        except Exception as e:
            print(' \n Error on line {}'.format(
                sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return json.dumps({"error": str(e.args)})
    # Validar valores del request
    def validate_values(self, request):
        for value_r in request:
            if value_r not in self.values_allow:
                return json.dumps({"code": 400, "message": f"Bad request: Value not allow [{value_r}]"})

        return False
