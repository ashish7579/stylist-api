from flask import Flask, request, jsonify
from stylist_core import generate_styling_for_product, generate_product_for_styling

app = Flask(__name__)

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

# ✅ Make it Replit-friendly by listening on 0.0.0.0:8000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
