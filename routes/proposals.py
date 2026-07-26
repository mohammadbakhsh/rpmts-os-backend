from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService
from services.ai_service import AIService

bp = Blueprint('proposals', __name__)
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
def get_proposals():
    """Get all proposals for the current user"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('proposals').select('*').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<proposal_id>', methods=['GET'])
def get_proposal(proposal_id):
    """Get a specific proposal"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('proposals').select('*').eq('id', proposal_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Proposal not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_proposal():
    """Create a new proposal"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['user_id'] = user_id
        response = supabase.query('proposals').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/generate', methods=['POST'])
def generate_proposal():
    """Generate a proposal using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        client_name = data.get('client_name')
        company_name = data.get('company_name')
        focus_areas = data.get('focus_areas')
        provider = data.get('provider', 'deepseek')
        
        result = ai_service.generate_proposal(client_name, company_name, focus_areas, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<proposal_id>', methods=['PUT'])
def update_proposal(proposal_id):
    """Update a proposal"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data.pop('user_id', None)
        response = supabase.query('proposals').update(data).eq('id', proposal_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Proposal not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400