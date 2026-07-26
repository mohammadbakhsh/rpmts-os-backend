from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService
from services.ai_service import AIService

bp = Blueprint('seo', __name__)
supabase = SupabaseService()
ai_service = AIService()

def get_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    user = supabase.get_user(token)
    return user.user.id if user else None

@bp.route('/analyze', methods=['POST'])
def analyze_seo():
    """Analyze SEO for a website"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        url = data.get('url')
        provider = data.get('provider', 'deepseek')
        
        if not url:
            return jsonify({'error': 'URL required'}), 400
        
        result = ai_service.analyze_seo(url, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/keywords', methods=['POST'])
def get_keywords():
    """Generate SEO keywords"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        topic = data.get('topic')
        provider = data.get('provider', 'deepseek')
        
        if not topic:
            return jsonify({'error': 'Topic required'}), 400
        
        prompt = f"Generate 20 SEO keywords for: {topic}"
        result = ai_service.generate(prompt, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/content', methods=['POST'])
def generate_seo_content():
    """Generate SEO-optimized content"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        topic = data.get('topic')
        keywords = data.get('keywords', [])
        provider = data.get('provider', 'deepseek')
        
        if not topic:
            return jsonify({'error': 'Topic required'}), 400
        
        prompt = f"""Write SEO-optimized content about: {topic}
        Target Keywords: {', '.join(keywords)}
        Include: Introduction, main content with headings, conclusion, and SEO meta description."""
        
        result = ai_service.generate(prompt, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400