from flask import Flask, Response, render_template, request, jsonify, make_response
from src.Search import search_in_reversed_index, find_news_by_title, mark_searched_words_in_content
from src.Indexation import create_compressed_trie_from_raw_files

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

@app.route('/get_news', methods=['GET'])
def get_news() -> Response:
    news_title: str = request.args.get('title', '')
    searched_words: str = request.args.get('searched_words', '')

    news: dict | None = find_news_by_title(news_title)
    if news is None:
        news = {"title": "News not found", "content": "The requested news article could not be found."}
    
    news['content'] = news['content'].lstrip('\n')
    news['content'] = news['content'].replace('\n', '<br>')
    news['content'] = mark_searched_words_in_content(news['content'], searched_words)

    response: Response = make_response(jsonify(news), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    create_compressed_trie_from_raw_files()
    app.run(host='127.0.0.1', port=5000, debug=True)
