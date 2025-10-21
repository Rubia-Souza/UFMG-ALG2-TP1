from flask import Flask, Response, render_template, request, jsonify, make_response
from src.Search import search_in_reversed_index

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home() -> str:
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search() -> Response:
    expression: str = request.args.get('expression', '')
    if not expression:
        response: Response = make_response(jsonify([{"title": "No results found", "snippet": ""}]), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    results: list[dict] | None = search_in_reversed_index(expression)
    if results is None:
        results = [{"title": "No results found", "snippet": ""}]
    
    response: Response = make_response(jsonify(results), 200)
    response.headers['Content-Type'] = 'application/json'

    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
