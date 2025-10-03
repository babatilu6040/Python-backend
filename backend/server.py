from flask import Flask
from flask_cors import CORS
from app.routes.search import search_bp

app = Flask(__name__)
CORS(app)  # enable CORS for frontend requests

# Register blueprint
app.register_blueprint(search_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)
    