from flask import Blueprint, jsonify, request
from services.supabase import SupabaseService

bp = Blueprint('dashboard', __name__)
supabase = SupabaseService()

def get_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header: return None
    token = auth_header.replace('Bearer ', '')
    user = supabase.get_user(token)
    return user.user.id if user else None

@bp.route('/stats', methods=['GET'])
def get_stats():
    user_id = get_user_id()
    if not user_id: return jsonify({'error': 'Unauthorized'}), 401

    # Use count='exact' to get count in response
    clients = supabase.query('clients').select('id', count='exact').eq('user_id', user_id).execute()
    projects = supabase.query('projects').select('id', count='exact').eq('user_id', user_id).eq('status', 'active').execute()
    invoices = supabase.query('invoices').select('id', count='exact').eq('user_id', user_id).execute()
    leads = supabase.query('leads').select('id', count='exact').eq('user_id', user_id).execute()
    revenue_result = supabase.query('invoices').select('total').eq('user_id', user_id).eq('status', 'paid').execute()
    revenue = sum([(i.get('total') or 0) for i in revenue_result.data])
    active_clients = supabase.query('clients').select('id', count='exact').eq('user_id', user_id).eq('status', 'active').execute()

    recent = supabase.query('clients').select('name, status, created_at').eq('user_id', user_id).order('created_at', desc=True).limit(5).execute()
    activity = [{'client': c.get('name',''), 'action': 'Client added', 'status': c.get('status','new'), 'date': c.get('created_at','')[:10] if c.get('created_at') else ''} for c in recent.data]

    return jsonify({
        'clients': clients.count if hasattr(clients, 'count') else len(clients.data),
        'active_projects': projects.count if hasattr(projects, 'count') else len(projects.data),
        'invoices': invoices.count if hasattr(invoices, 'count') else len(invoices.data),
        'leads': leads.count if hasattr(leads, 'count') else len(leads.data),
        'revenue': revenue,
        'active_clients': active_clients.count if hasattr(active_clients, 'count') else len(active_clients.data),
        'recent_activity': activity
    })