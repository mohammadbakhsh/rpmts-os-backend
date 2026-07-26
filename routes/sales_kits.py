from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService
from services.ai_service import AIService

bp = Blueprint('sales_kits', __name__)
supabase = SupabaseService()
ai_service = AIService()

def get_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    user = supabase.get_user(token)
    return user.user.id if user else None

@bp.route('/', methods=['GET'])
def get_sales_kits():
    """Get all sales kits for the current user"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('sales_kits').select('*').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_sales_kit():
    """Create a new sales kit"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['user_id'] = user_id
        response = supabase.query('sales_kits').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/generate', methods=['POST'])
def generate_sales_kit():
    """Generate a sales kit using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        name = data.get('name')
        audience = data.get('audience')
        format_type = data.get('format', 'intro')
        provider = data.get('provider', 'deepseek')
        
        result = ai_service.generate_sales_kit(name, audience, format_type, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<kit_id>', methods=['PUT'])
def update_sales_kit(kit_id):
    """Update a sales kit"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data.pop('user_id', None)
        response = supabase.query('sales_kits').update(data).eq('id', kit_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Sales kit not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400