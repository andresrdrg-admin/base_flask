from flask import request, Response
from controllers.cron_controller import CronController

class RoutesExample():
    def __init__(self, app) -> None:
        @app.route("/example", methods=['GET'])
        def example_function():
            return Response({}, mimetype='application/json')