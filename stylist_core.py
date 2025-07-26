import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Setup API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Catalog cache system
catalog_cache = {
    "data": None,
    "last_updated": None
}

def fetch_catalog():
    sheet_csv_url = "https://docs.google.com/spreadsheets/d/1sJ_w4BkJha3SN4H6Eo-Fr-WqyytmryDU4sBOZeUwmHM/export?format=csv"
    if catalog_cache["data"] is None or datetime.now() - catalog_cache["last_updated"] > timedelta(minutes=60):
        catalog_cache["data"] = pd.read_csv(sheet_csv_url)
        catalog_cache["last_updated"] = datetime.now()
    return catalog_cache["data"]

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

def generate_styling_for_product(product_data):
    prompt = f"""
You are a professional jewellery stylist. Based on the product below, suggest:
- Occasion
- Mood
- Outfit Type
- Neckline
- Hairstyle

Product:
Category: {product_data.get('category')}
Metal Color: {product_data.get('metal_color')}
Stone/Enamel Color: {product_data.get('stone_color')}
"""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def generate_product_for_styling(styling_context):
    prompt = f"""
Based on this style context, suggest:
- Jewellery Category
- Metal Color
- Stone/Enamel Color
- Product Description

Style:
Occasion: {styling_context.get('occasion')}
Mood: {styling_context.get('mood')}
Outfit: {styling_context.get('outfit')}
Neckline: {styling_context.get('neckline')}
Hairstyle: {styling_context.get('hairstyle')}
"""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text
