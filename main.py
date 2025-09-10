# main.py
from fastapi import FastAPI, Request
from lxml import etree
from bs4 import BeautifulSoup
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

def clean_html_and_get_text(html_content):
    """Safely cleans HTML and returns plain text."""
    if not html_content or not isinstance(html_content, str):
        return ""
    soup = BeautifulSoup(html_content, 'lxml')
    return soup.get_text(separator=' ', strip=True)

def element_to_dict(element):
    """
    Recursively converts an XML element and its children into a clean dictionary.
    This version correctly handles nested tags and lists.
    """
    # Base case: If the element has no children, return its cleaned text
    if not list(element):
        return clean_html_and_get_text(element.text)

    # Recursive step: Process child elements
    result = {}
    for child in element:
        child_data = element_to_dict(child)
        
        # If the tag name already exists, we have a list of items
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]  # Convert existing item to a list
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data
            
    return result

def extract_all_available_products(xml_string: str) -> list[dict]:
    """
    Processes a raw XML string to extract, clean, and filter product data.
    """
    try:
        parser = etree.XMLParser(recover=True, encoding='utf-8')
        tree = etree.fromstring(xml_string.encode('utf-8'), parser=parser)
        
        all_products = tree.xpath('//product')
        logging.info(f"Found {len(all_products)} total products to process.")
        
        available_products_data = []
        for product in all_products:
            # 1. Filter: Check if the product is available
            availability_node = product.find('Availability')
            if availability_node is None or not (availability_node.text and availability_node.text.strip().lower() == 'yes'):
                continue # Skip to the next product if not available

            # 2. Convert the entire <product> element into a clean dictionary
            product_dict = element_to_dict(product)
            available_products_data.append(product_dict)
                    
        logging.info(f"Returning full data for {len(available_products_data)} clean and available products.")
        return available_products_data
        
    except Exception as e:
        logging.error(f"XML Processing Error: {e}")
        return []


@app.get("/")
def read_root():
    return {"status": "API is running"}


@app.post("/chunk")
async def process_data(request: Request):
    """
    This endpoint receives raw XML, filters it, cleans it, and returns
    a full but structured JSON object for each available product.
    """
    logging.info("--- New request received ---")
    
    body = await request.body()
    raw_text = body.decode('utf-8', errors='ignore')
    
    # Process, filter, and extract all data from the XML
    clean_product_list = extract_all_available_products(raw_text)
    
    # Return the final, clean list of full product objects
    return {"products": clean_product_list}
