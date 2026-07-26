from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService

bp = Blueprint('network', __name__)
supabase = SupabaseService()

def get_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    user = supabase.get_user(token)
    return user.user.id if user else None

@bp.route('/connections', methods=['GET'])
def get_connections():
    """Get all network connections for the current user"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('network_connections').select('*').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/connections', methods=['POST'])
def create_connection():
    """Create a new network connection"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['user_id'] = user_id
        response = supabase.query('network_connections').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/connections/<connection_id>', methods=['PUT'])
def update_connection(connection_id):
    """Update a network connection"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data.pop('user_id', None)
        response = supabase.query('network_connections').update(data).eq('id', connection_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Connection not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/connections/<connection_id>', methods=['DELETE'])
def delete_connection(connection_id):
    """Delete a network connection"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('network_connections').delete().eq('id', connection_id).eq('user_id', user_id).execute()
        return jsonify({'message': 'Connection deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400