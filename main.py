# main.py
from fastapi import FastAPI, Request
from lxml import etree
from bs4 import BeautifulSoup
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

def extract_and_clean_products(xml_string: str) -> list[dict]:
    """
    Processes a raw XML string to extract, clean, and filter product data.
    """
    try:
        parser = etree.XMLParser(recover=True, encoding='utf-8')
        tree = etree.fromstring(xml_string.encode('utf-8'), parser=parser)
        
        all_products = tree.xpath('//product')
        logging.info(f"Found {len(all_products)} total products to process.")
        
        clean_products = []
        for product in all_products:
            availability_node = product.find('Availability')
            if availability_node is None or not (availability_node.text and availability_node.text.strip().lower() == 'yes'):
                continue

            name_node = product.find('FranchiseName')
            short_desc_node = product.find('ShortDescription')
            detailed_desc_node = product.find('DetailedDescription')
            
            name = name_node.text if name_node is not None else ""
            
            # --- THIS IS THE PART THAT HAS BEEN FIXED ---
            # Using 'or ""' provides a safe default if the tag is empty (text is None)
            short_desc_html = short_desc_node.text or ""
            detailed_desc_html = detailed_desc_node.text or ""

            # Clean the descriptions using BeautifulSoup
            short_desc_text = BeautifulSoup(short_desc_html, 'lxml').get_text(separator=' ', strip=True)
            detailed_desc_text = BeautifulSoup(detailed_desc_html, 'lxml').get_text(separator=' ', strip=True)
            
            full_description = f"{short_desc_text} {detailed_desc_text}".strip()

            if name and full_description:
                clean_products.append({
                    "name": name.strip(),
                    "description": full_description
                })
                    
        logging.info(f"Returning {len(clean_products)} clean and available products.")
        return clean_products
        
    except Exception as e:
        logging.error(f"XML Processing Error: {e}")
        return []


@app.get("/")
def read_root():
    return {"status": "API is running"}


@app.post("/chunk")
async def process_data(request: Request):
    """
    This endpoint receives raw XML, filters it, cleans it, extracts key fields,
    and returns a simple JSON array of objects.
    """
    logging.info("--- New request received ---")
    
    body = await request.body()
    raw_text = body.decode('utf-8', errors='ignore')
    
    clean_product_list = extract_and_clean_products(raw_text)
    
    return {"products": clean_product_list}