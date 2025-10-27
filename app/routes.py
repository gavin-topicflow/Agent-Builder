from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@bp.route('/api/hello', methods=['GET', 'POST'])
def api_hello():
    """Simple API endpoint"""
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', 'World')
    else:
        name = request.args.get('name', 'World')

    return jsonify({
        'message': f'Hello, {name}!',
        'status': 'success'
    })
