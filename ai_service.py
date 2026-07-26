import json
import requests
from config import Config

class AIService:
    def __init__(self):
        self.providers = {
            'deepseek': {
                'endpoint': Config.DEEPSEEK_ENDPOINT,
                'api_key': Config.DEEPSEEK_API_KEY,
                'model': Config.DEEPSEEK_MODEL,
                'headers': {'Content-Type': 'application/json', 'Authorization': f'Bearer {Config.DEEPSEEK_API_KEY}'}
            },
            'openai': {
                'endpoint': 'https://api.openai.com/v1/chat/completions',
                'api_key': Config.OPENAI_API_KEY,
                'model': Config.OPENAI_MODEL,
                'headers': {'Content-Type': 'application/json', 'Authorization': f'Bearer {Config.OPENAI_API_KEY}'}
            },
            'groq': {
                'endpoint': 'https://api.groq.com/openai/v1/chat/completions',
                'api_key': Config.GROQ_API_KEY,
                'model': Config.GROQ_MODEL,
                'headers': {'Content-Type': 'application/json', 'Authorization': f'Bearer {Config.GROQ_API_KEY}'}
            }
        }

    def get_provider(self, provider_name='deepseek'):
        return self.providers.get(provider_name, self.providers['deepseek'])

    def generate(self, prompt: str, provider: str = 'deepseek', temperature: float = 0.7, max_tokens: int = 2000):
        provider_config = self.get_provider(provider)
        if not provider_config or not provider_config.get('api_key'):
            return {'error': f'API key for {provider} not configured'}
        payload = {
            'model': provider_config['model'],
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant for a corporate training company called RPM Training Solutions.'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        try:
            response = requests.post(provider_config['endpoint'], headers=provider_config['headers'], json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            return {'success': True, 'content': content, 'raw': result}
        except Exception as e:
            return {'error': str(e)}

    # ---- AI feature methods ----
    def search_companies(self, sector, city, size, count=10, provider='deepseek'):
        prompt = f"""Search for {count} companies in the {sector} sector in {city} with company size {size}.
        For each, provide: name, sector, city, size, contact_name, contact_email, suggested_services.
        Return as JSON array with those fields."""
        result = self.generate(prompt, provider)
        if result.get('success'):
            try:
                import re
                content = result['content']
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    companies = json.loads(json_match.group())
                    return {'success': True, 'companies': companies}
            except: pass
            return {'success': True, 'companies': []}
        return result

    def generate_proposal(self, client_name, company_name, focus_areas, provider='deepseek'):
        prompt = f"""Create a professional proposal for RPM Training Solutions.
        Client: {client_name}, Company: {company_name}, Focus: {focus_areas}.
        Include: Executive Summary, Business Needs, Proposed Solutions, Timeline, Investment."""
        return self.generate(prompt, provider)

    def generate_email(self, client_name, company_name, purpose, key_points, cta, provider='deepseek'):
        prompt = f"""Write a professional email to {client_name} at {company_name}.
        Purpose: {purpose}. Key points: {key_points}. CTA: {cta}.
        Include subject line. Keep 150-250 words."""
        return self.generate(prompt, provider)

    def analyze_competitor(self, competitor_name, industry, provider='deepseek'):
        prompt = f"""Analyze {competitor_name} in {industry}. Provide strengths, weaknesses, services, opportunities, and strategic analysis.
        Return JSON with fields: strengths (array), weaknesses (array), services (array), opportunities (array), analysis (string)."""
        result = self.generate(prompt, provider)
        if result.get('success'):
            try:
                import re
                content = result['content']
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    return {'success': True, **data}
            except: pass
            return {'success': True, 'analysis': result['content']}
        return result

    def generate_reply(self, client_name, review_text, rating, provider='deepseek'):
        prompt = f"""Write a professional reply to a {rating}/5 review from {client_name}:
        "{review_text}"
        Reply should be thankful, professional, address concerns, end positively. Keep 100-150 words."""
        return self.generate(prompt, provider)

    def analyze_seo(self, url, provider='deepseek'):
        prompt = f"""Analyze {url} for SEO. Provide summary and 5-10 specific recommendations with priority (high/medium/low).
        Return JSON with fields: summary (string), recommendations (array of {text, priority})."""
        result = self.generate(prompt, provider)
        if result.get('success'):
            try:
                import re
                content = result['content']
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    return {'success': True, 'analysis': data}
            except: pass
            return {'success': True, 'analysis': {'summary': result['content'], 'recommendations': []}}
        return result

    def generate_sales_kit(self, name, audience, format_type='intro', provider='deepseek'):
        prompt = f"""Create a sales kit for RPM Training Solutions.
        Name: {name}, Audience: {audience}, Format: {format_type}.
        Include: Company intro, key services, value proposition, success stories, CTA."""
        return self.generate(prompt, provider)

    def generate_content(self, topic, content_type='draft', provider='deepseek'):
        prompt = f"""Create {content_type} content about: {topic}. Professional, structured, 400-600 words."""
        return self.generate(prompt, provider)

    def prospect_companies(self, industry, count=5, provider='deepseek'):
        prompt = f"""Find {count} potential clients in {industry}. For each: company_name, industry, website, contact_name, contact_email, reason, analysis.
        Return JSON array."""
        result = self.generate(prompt, provider)
        if result.get('success'):
            try:
                import re
                content = result['content']
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    leads = json.loads(json_match.group())
                    return {'success': True, 'leads': leads}
            except: pass
            return {'success': True, 'leads': []}
        return result

    def test_connection(self, provider, api_key=None):
        if api_key and provider in self.providers:
            self.providers[provider]['api_key'] = api_key
            self.providers[provider]['headers']['Authorization'] = f'Bearer {api_key}'
        return self.generate('Say "Connection successful!" in one sentence.', provider)