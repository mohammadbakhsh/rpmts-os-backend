from flask import Blueprint, request, jsonify
from services.supabase import SupabaseService
from services.ai_service import AIService

bp = Blueprint('ai', __name__)
supabase = SupabaseService()
ai_service = AIService()


def get_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.replace('Bearer ', '')
    user = supabase.get_user(token)
    return user.user.id if user else None


@bp.route('/generate', methods=['POST'])
def generate():
    """Generic AI generation endpoint"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        prompt = data.get('prompt')
        provider = data.get('provider', 'deepseek')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 2000)

        if not prompt:
            return jsonify({'error': 'Prompt required'}), 400

        result = ai_service.generate(prompt, provider, temperature, max_tokens)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/email', methods=['POST'])
def generate_email():
    """Generate a professional email using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        client_name = data.get('client_name')
        company_name = data.get('company_name')
        purpose = data.get('purpose')
        key_points = data.get('key_points')
        cta = data.get('cta')
        provider = data.get('provider', 'deepseek')

        result = ai_service.generate_email(
            client_name, company_name, purpose, key_points, cta, provider
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/content', methods=['POST'])
def generate_content():
    """Generate general content using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        topic = data.get('topic')
        content_type = data.get('content_type', 'draft')
        provider = data.get('provider', 'deepseek')

        if not topic:
            return jsonify({'error': 'Topic required'}), 400

        result = ai_service.generate_content(topic, content_type, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/search-companies', methods=['POST'])
def search_companies():
    """Search for companies using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        sector = data.get('sector')
        city = data.get('city')
        size = data.get('size')
        count = data.get('count', 10)
        provider = data.get('provider', 'deepseek')

        result = ai_service.search_companies(sector, city, size, count, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/prospect', methods=['POST'])
def prospect_companies():
    """Prospect potential client companies using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        industry = data.get('industry')
        count = data.get('count', 5)
        provider = data.get('provider', 'deepseek')

        if not industry:
            return jsonify({'error': 'Industry required'}), 400

        result = ai_service.prospect_companies(industry, count, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/proposal', methods=['POST'])
def generate_proposal():
    """Generate a proposal using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        client_name = data.get('client_name')
        company_name = data.get('company_name')
        focus_areas = data.get('focus_areas')
        provider = data.get('provider', 'deepseek')

        result = ai_service.generate_proposal(
            client_name, company_name, focus_areas, provider
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/analyze-competitor', methods=['POST'])
def analyze_competitor():
    """Analyze a competitor using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        competitor_name = data.get('competitor_name')
        industry = data.get('industry')
        provider = data.get('provider', 'deepseek')

        if not competitor_name:
            return jsonify({'error': 'Competitor name required'}), 400

        result = ai_service.analyze_competitor(competitor_name, industry, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/reply', methods=['POST'])
def generate_reply():
    """Generate a reply to a client review using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        client_name = data.get('client_name')
        review_text = data.get('review_text')
        rating = data.get('rating', 5)
        provider = data.get('provider', 'deepseek')

        result = ai_service.generate_reply(client_name, review_text, rating, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/analyze-seo', methods=['POST'])
def analyze_seo():
    """Analyze a website for SEO using AI"""
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


@bp.route('/sales-kit', methods=['POST'])
def generate_sales_kit():
    """Generate a sales kit using AI"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        name = data.get('name')
        audience = data.get('audience')
        format_type = data.get('format', 'intro')
        provider = data.get('provider', 'deepseek')

        result = ai_service.generate_sales_kit(name, audience, format_type, provider)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/test', methods=['POST'])
def test_connection():
    """Test an AI provider connection"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json() or {}
        provider = data.get('provider', 'deepseek')
        api_key = data.get('api_key')

        result = ai_service.test_connection(provider, api_key)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
