from sqlalchemy import inspect


class BaseModel():
    def __init__(self) -> None:
        pass

    def as_array(self):
        columns_model = []
        for column in (inspect(self)).attrs:
            columns_model.append(column.key)
        return columns_model

    def as_dict(self):
        columns_model = {}
        for column in (inspect(self)).attrs:
            if column.key in self.__table__.columns:
                columns_model[column.key] = (
                    str(column.value) if "date" in column.key else column.value
                )
        return columns_model

    def __repr__(self):
        values = str(self.as_dict())
        return f"{self.__tablename__}_model({values})"
