from flask_restx import Resource, Namespace


class APIResource(Resource):
    def __init__(self, api):
        Resource.__init__(self, api)


class NameSpace(Namespace):
    def __init__(self, ns):
        Namespace.__init__(self, ns)
