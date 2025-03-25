from flask import Blueprint ,  request , jsonify
from ..services.health_service import HealthService
health_bp = Blueprint('health' , __name__)
@health_bp.route('/health', methods=['GET'])
def get_health_all():
    health =  HealthService.get_health_all()
    return jsonify(health) , 200


