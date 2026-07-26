from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService

bp = Blueprint('invoices', __name__)
supabase = SupabaseService()

def get_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    user = supabase.get_user(token)
    return user.user.id if user else None

@bp.route('/', methods=['GET'])
def get_invoices():
    """Get all invoices for the current user"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('invoices').select('*').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """Get a specific invoice"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('invoices').select('*').eq('id', invoice_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Invoice not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_invoice():
    """Create a new invoice"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['user_id'] = user_id
        response = supabase.query('invoices').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    """Update an invoice"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data.pop('user_id', None)
        response = supabase.query('invoices').update(data).eq('id', invoice_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Invoice not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<invoice_id>/pay', methods=['POST'])
def mark_paid(invoice_id):
    """Mark invoice as paid"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('invoices').update({'status': 'paid'}).eq('id', invoice_id).eq('user_id', user_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({'error': 'Invoice not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    """Delete an invoice"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('invoices').delete().eq('id', invoice_id).eq('user_id', user_id).execute()
        return jsonify({'message': 'Invoice deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400