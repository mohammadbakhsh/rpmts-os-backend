from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService

bp = Blueprint('projects', __name__)
supabase = SupabaseService()

def get_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    user = supabase.get_user(token)
    return user.user.id if user else None

@bp.route('/', methods=['GET'])
def get_projects():
    """Get all projects for the current user"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('projects').select('*').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('projects').select('*').eq('id', project_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Project not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_project():
    """Create a new project"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['user_id'] = user_id
        response = supabase.query('projects').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Update a project"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        # Remove user_id from data to prevent overriding
        data.pop('user_id', None)
        response = supabase.query('projects').update(data).eq('id', project_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Project not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('projects').delete().eq('id', project_id).eq('user_id', user_id).execute()
        return jsonify({'message': 'Project deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400