from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService

bp = Blueprint('auth', __name__)
supabase = SupabaseService()

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name', '')
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    try:
        response = supabase.client.auth.sign_up({
            'email': email,
            'password': password,
            'options': {'data': {'full_name': full_name}}
        })
        if response.user:
            return jsonify({
                'success': True,
                'user': {'id': response.user.id, 'email': email, 'full_name': full_name}
            })
        return jsonify({'error': 'Signup failed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    try:
        response = supabase.client.auth.sign_in_with_password({'email': email, 'password': password})
        if response.user and response.session:
            return jsonify({
                'success': True,
                'token': response.session.access_token,
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    'full_name': response.user.user_metadata.get('full_name', '')
                }
            })
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/me', methods=['GET'])
def me():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'No token provided'}), 401
    token = auth_header.replace('Bearer ', '')
    try:
        user = supabase.get_user(token)
        if user:
            return jsonify({
                'id': user.user.id,
                'email': user.user.email,
                'full_name': user.user.user_metadata.get('full_name', '')
            })
        return jsonify({'error': 'Invalid token'}), 401
    except:
        return jsonify({'error': 'Invalid token'}), 401