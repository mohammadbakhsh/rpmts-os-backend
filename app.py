from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes import (
    auth, clients, projects, invoices, leads, proposals, campaigns,
    targets, sales_kits, briefs, productions, publishing,
    reviews, seo, network, competitors, dashboard, ai
)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=Config.CORS_ORIGINS)

app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(clients.bp, url_prefix='/api/clients')
app.register_blueprint(projects.bp, url_prefix='/api/projects')
app.register_blueprint(invoices.bp, url_prefix='/api/invoices')
app.register_blueprint(leads.bp, url_prefix='/api/leads')
app.register_blueprint(proposals.bp, url_prefix='/api/proposals')
app.register_blueprint(campaigns.bp, url_prefix='/api/campaigns')
app.register_blueprint(targets.bp, url_prefix='/api/targets')
app.register_blueprint(sales_kits.bp, url_prefix='/api/sales-kits')
app.register_blueprint(briefs.bp, url_prefix='/api/briefs')
app.register_blueprint(productions.bp, url_prefix='/api/productions')
app.register_blueprint(publishing.bp, url_prefix='/api/publishing')
app.register_blueprint(reviews.bp, url_prefix='/api/reviews')
app.register_blueprint(seo.bp, url_prefix='/api/seo')
app.register_blueprint(network.bp, url_prefix='/api/network')
app.register_blueprint(competitors.bp, url_prefix='/api/competitors')
app.register_blueprint(dashboard.bp, url_prefix='/api/dashboard')
app.register_blueprint(ai.bp, url_prefix='/api/ai')

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'message': 'RPM OS API is running'})

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=5000)