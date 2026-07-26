from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService

bp = Blueprint('targets', __name__)
supabase = SupabaseService()

def get_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    user = supabase.get_user(token)
    return user.user.id if user else None

@bp.route('/', methods=['GET'])
def get_targets():
    """Get all targets for the current user"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('targets').select('*').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_target():
    """Create a new target"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['user_id'] = user_id
        response = supabase.query('targets').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<target_id>', methods=['PUT'])
def update_target(target_id):
    """Update a target"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data.pop('user_id', None)
        response = supabase.query('targets').update(data).eq('id', target_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Target not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<target_id>', methods=['DELETE'])
def delete_target(target_id):
    """Delete a target"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('targets').delete().eq('id', target_id).eq('user_id', user_id).execute()
        return jsonify({'message': 'Target deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400