from flask import Flask, request, jsonify
from flask_cors import CORS
from stylist_core import generate_styling_for_product, generate_product_for_styling
import os

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all domains

# Your endpoints follow here...

@app.route('/')
def home():
    return "Stylist API is running."

@app.route('/product-to-style', methods=['POST'])
def product_to_style():
    data = request.json
    product_id = data.get('product_id')
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    result = generate_styling_for_product(product_id)
    return jsonify({'result': result})

@app.route('/style-to-product', methods=['POST'])
def style_to_product():
    data = request.json
    style_context = data.get('style_context')
    if not style_context:
        return jsonify({'error': 'Style context is required'}), 400
    result = generate_product_for_styling(style_context)
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
