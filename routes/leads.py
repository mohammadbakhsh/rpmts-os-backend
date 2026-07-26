from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService
from services.ai_service import AIService

bp = Blueprint('leads', __name__)
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
def get_leads():
    """Get all leads for the current user"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('leads').select('*').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get a specific lead"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('leads').select('*').eq('id', lead_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Lead not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_lead():
    """Create a new lead"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['user_id'] = user_id
        response = supabase.query('leads').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """Update a lead"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data.pop('user_id', None)
        response = supabase.query('leads').update(data).eq('id', lead_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Lead not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<lead_id>/convert', methods=['POST'])
def convert_lead(lead_id):
    """Convert lead to client"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Get lead data
        lead_response = supabase.query('leads').select('*').eq('id', lead_id).eq('user_id', user_id).execute()
        if not lead_response.data:
            return jsonify({'error': 'Lead not found'}), 404
        
        lead = lead_response.data[0]
        
        # Create client from lead
        client_data = {
            'name': lead.get('name'),
            'email': lead.get('email'),
            'phone': lead.get('phone'),
            'company': lead.get('company'),
            'status': 'active',
            'user_id': user_id
        }
        client_response = supabase.query('clients').insert(client_data).execute()
        
        # Update lead status
        supabase.query('leads').update({'status': 'converted'}).eq('id', lead_id).eq('user_id', user_id).execute()
        
        return jsonify({
            'message': 'Lead converted to client successfully',
            'client': client_response.data[0]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    """Delete a lead"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('leads').delete().eq('id', lead_id).eq('user_id', user_id).execute()
        return jsonify({'message': 'Lead deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400