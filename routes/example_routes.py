from flask import request, Response

class RoutesExample():
    def __init__(self, app) -> None:
        @app.route("/example", methods=['GET'])
        def example_function():
            return Response({}, mimetype='application/json')
