from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService
from services.ai_service import AIService

bp = Blueprint('competitors', __name__)
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
def get_competitors():
    """Get all competitors for the current user"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('competitors').select('*').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<competitor_id>', methods=['GET'])
def get_competitor(competitor_id):
    """Get a specific competitor"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('competitors').select('*').eq('id', competitor_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Competitor not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_competitor():
    """Create a new competitor"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['user_id'] = user_id
        response = supabase.query('competitors').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/analyze', methods=['POST'])
def analyze_competitor():
    """Analyze a competitor using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        competitor_name = data.get('competitor_name')
        industry = data.get('industry')
        provider = data.get('provider', 'deepseek')
        
        if not competitor_name:
            return jsonify({'error': 'Competitor name required'}), 400
        
        result = ai_service.analyze_competitor(competitor_name, industry, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<competitor_id>', methods=['PUT'])
def update_competitor(competitor_id):
    """Update a competitor"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data.pop('user_id', None)
        response = supabase.query('competitors').update(data).eq('id', competitor_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Competitor not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<competitor_id>', methods=['DELETE'])
def delete_competitor(competitor_id):
    """Delete a competitor"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('competitors').delete().eq('id', competitor_id).eq('user_id', user_id).execute()
        return jsonify({'message': 'Competitor deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400