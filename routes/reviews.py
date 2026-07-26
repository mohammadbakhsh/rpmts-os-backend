from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService
from services.ai_service import AIService

bp = Blueprint('reviews', __name__)
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
def get_reviews():
    """Get all reviews for the current user"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('reviews').select('*').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_review():
    """Create a new review"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['user_id'] = user_id
        response = supabase.query('reviews').insert(data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<review_id>/reply', methods=['POST'])
def generate_reply(review_id):
    """Generate AI reply to a review"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        # Get the review
        review_response = supabase.query('reviews').select('*').eq('id', review_id).eq('user_id', user_id).execute()
        if not review_response.data:
            return jsonify({'error': 'Review not found'}), 404
        
        review = review_response.data[0]
        client_name = review.get('client_name', 'Client')
        review_text = review.get('review_text', '')
        rating = review.get('rating', 5)
        provider = data.get('provider', 'deepseek')
        
        result = ai_service.generate_reply(client_name, review_text, rating, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        response = supabase.query('reviews').delete().eq('id', review_id).eq('user_id', user_id).execute()
        return jsonify({'message': 'Review deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400