XML Franchise Data Cleaner API
This is a simple yet powerful API built with Python and FastAPI. Its purpose is to receive a large, raw XML data feed, process it, and return a clean, simplified JSON output.

This service is designed to act as a data-cleaning middle layer for automation platforms like Make.com or n8n, saving on processing steps and costs.

Key Features
Receives Raw XML: Accepts a raw XML text body via a POST request.

Handles Messy Data: Uses a recovering parser to automatically fix common XML errors like unclosed tags.

Filters by Availability: Intelligently parses the XML and returns only the products where the <Availability> tag contains "Yes".

Extracts Specific Fields: Discards all unnecessary data and extracts only the FranchiseName, ShortDescription, and DetailedDescription.

Cleans HTML Content: Strips all HTML tags (<p>, <strong>, <span>, etc.) from the description fields, leaving only plain text.

Returns Clean JSON: Outputs a simple, clean JSON array of objects, perfect for use in other applications.

API Endpoint
POST /chunk
This is the main endpoint for processing the data.

Method: POST

Request Body: The raw XML content.

Headers: The Content-Type header should be set to application/xml or text/plain.

Example Response Body:
The API will return a JSON object containing a list of products. Each product is a simple object with just a name and description.

{
  "products": [
    {
      "name": "JETSET Pilates",
      "description": "JETSET Pilates is a modern studio offering an upscale experience... Founded in Miami in 2010..."
    },
    {
      "name": "Another Available Franchise",
      "description": "A clean, combined, and plain-text description for the second franchise goes here."
    }
  ]
}

Setup and Installation
1. Prerequisites
Python 3.8+

Git

2. Local Setup
Follow these steps to run the application on your local machine.

# 1. Clone the repository
git clone [https://github.com/zubairahmedi/chunks.git](https://github.com/zubairahmedi/chunks.git)

# 2. Navigate into the project directory
cd chunks

# 3. Install the required libraries
pip install -r requirements.txt

# 4. Run the development server
uvicorn main:app --reload

The API will now be running locally at http://127.0.0.1:8000.

Deployment (Render.com)
This application is ready to be deployed on a service like Render.

Push your code to your GitHub repository.

On Render, create a new "Web Service" and connect it to your GitHub repository.

Use the following settings during setup:

Build Command: pip install -r requirements.txt

Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

Render will automatically deploy your application and provide you with a public URL.
