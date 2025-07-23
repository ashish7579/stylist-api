# stylist_core.py

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_styling_for_product(product_data):
    prompt = f"""
    You are an expert fashion stylist. Based on the following product details, suggest suitable styling contexts:

    Product Details:
    - Category: {product_data.get('category')}
    - Metal Color: {product_data.get('metal_color')}
    - Stone/Enamel Color: {product_data.get('stone_color')}

    Respond in this format:
    Occasion:
    Mood:
    Outfit Type:
    Neckline:
    Hairstyle:
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def generate_product_for_styling(styling_context):
    prompt = f"""
    You are a jewellery stylist bot. Based on the following styling context, suggest jewellery product recommendations and categories.

    Styling Context:
    - Occasion: {styling_context.get('occasion')}
    - Mood: {styling_context.get('mood')}
    - Outfit Type: {styling_context.get('outfit')}
    - Neckline: {styling_context.get('neckline')}
    - Hairstyle: {styling_context.get('hairstyle')}

    Respond in this format:
    - Suggested Category:
    - Metal Color:
    - Stone/Enamel Color:
    - Suggested Description:
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
