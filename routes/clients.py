from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService

bp = Blueprint('clients', __name__)
supabase = SupabaseService()

def get_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    user = supabase.get_user(token)
    return user.user.id if user else None

@bp.route('/', methods=['GET'])
def get_clients():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    result = supabase.query('clients').select('*').eq('user_id', user_id).execute()
    return jsonify(result.data)

@bp.route('/<id>', methods=['GET'])
def get_client(id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    result = supabase.query('clients').select('*').eq('id', id).eq('user_id', user_id).execute()
    if not result.data:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify(result.data[0])

@bp.route('/', methods=['POST'])
def create_client():
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    data['user_id'] = user_id
    
    result = supabase.query('clients').insert(data).execute()
    return jsonify(result.data[0])

@bp.route('/<id>', methods=['PUT'])
def update_client(id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    data.pop('user_id', None)
    data.pop('id', None)
    data['updated_at'] = 'now()'
    
    result = supabase.query('clients').update(data).eq('id', id).eq('user_id', user_id).execute()
    if not result.data:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify(result.data[0])

@bp.route('/<id>', methods=['DELETE'])
def delete_client(id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    result = supabase.query('clients').delete().eq('id', id).eq('user_id', user_id).execute()
    return jsonify({'success': True})