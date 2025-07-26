import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Catalog caching
catalog_cache = {
    "data": None,
    "last_updated": None
}

def fetch_catalog():
    sheet_csv_url = "https://docs.google.com/spreadsheets/d/1sJ_w4BkJha3SN4H6Eo-Fr-WqyytmryDU4sBOZeUwmHM/export?format=csv"
    
    # Refresh every 60 mins
    if catalog_cache["data"] is None or datetime.now() - catalog_cache["last_updated"] > timedelta(minutes=60):
        catalog_cache["data"] = pd.read_csv(sheet_csv_url)
        catalog_cache["last_updated"] = datetime.now()
    
    return catalog_cache["data"]

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
    model = genai.GenerativeModel(model_name="models/gemini-pro")  # ✅ Correct version now
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
    model = genai.GenerativeModel(model_name="models/gemini-pro")  # ✅ Correct version now
    response = model.generate_content(prompt)
    return response.text

def get_product_data(product_id):
    catalog = fetch_catalog()
    row = catalog[catalog["Product ID"] == product_id.upper()]
    if row.empty:
        return None
    return {
        "category": row.iloc[0]["Category"],
        "metal_color": row.iloc[0]["Metal Color"],
        "stone_color": row.iloc[0]["Stone/Enamel Color"]
    }
