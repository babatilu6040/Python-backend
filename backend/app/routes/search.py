from flask import Blueprint, request, jsonify
import requests
from app.module.query_handler import queryhandler
import asyncio
search_bp = Blueprint("search", __name__)
@search_bp.route("/api/search/result", methods=["POST"])


def search_result():
    print("\n")
    data = request.get_json()
    query = data.get("q")
    print("🔍 Received query:", query)
    
    if not query:
        return jsonify({
            "status": "error",
            "message": "Missing 'q' in request data."
        }), 400
    result = asyncio.run(queryhandler(query))
    
  
    return jsonify({
        "status": "success",
        "data": result
    })
