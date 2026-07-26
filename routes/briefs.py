from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService

bp = Blueprint('briefs', __name__)
supabase = SupabaseService()

def get_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    user = supabase.get_user(token)
    return user.user.id if user else None

@bp.route('/', methods=['GET'])
def get_briefs():
    """Get all briefs for the current user"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('briefs').select('*').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<brief_id>', methods=['GET'])
def get_brief(brief_id):
    """Get a specific brief"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('briefs').select('*').eq('id', brief_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Brief not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_brief():
    """Create a new brief"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['user_id'] = user_id
        response = supabase.query('briefs').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<brief_id>', methods=['PUT'])
def update_brief(brief_id):
    """Update a brief"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data.pop('user_id', None)
        response = supabase.query('briefs').update(data).eq('id', brief_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Brief not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<brief_id>', methods=['DELETE'])
def delete_brief(brief_id):
    """Delete a brief"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('briefs').delete().eq('id', brief_id).eq('user_id', user_id).execute()
        return jsonify({'message': 'Brief deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400