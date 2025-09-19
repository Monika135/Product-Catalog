from .Resource import APIResource
from flask import current_app


class HealthCheck(APIResource):

    def get(self):
        try:
            return {"message": "SUCCESS"}, 200

        except Exception as e:
            current_app.error_logger.error("error in HealthCheck", exc_info=e)
            return {"message": 'error in health check'}, 400
