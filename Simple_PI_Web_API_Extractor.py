import os
import json
import requests
from loguru import logger
from dotenv import load_dotenv
from pathlib import Path
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()

# Constants
HTTP_STATUS_OK = 200
BASE_DIR = Path(__file__).resolve().parent

# Environment variable for PI Web API server URL
PIWEBAPI_URL = os.getenv("PIWEBAPI_LOCAL", "default")
PIWEBAPI_USERNAME = os.getenv("PIUSERNAME_LOCAL", "default")
PIWEBAPI_PASS = os.getenv("PIPASSWORD_LOCAL", "default")

# Logging configuration
logger.remove()
logger.add(
    f"{BASE_DIR}/logs/app.log",
    format="[{time:YYYY-MM-DD HH:mm:ss}] <lvl>:: {level:<8} :: {line:<4}:{function:<18} - {message}</lvl>",
    rotation="5 MB",
    level=os.getenv("LOG_LEVEL", "WARNING"),
)

class SimplePIDataExtractor:
    def __init__(self):
        self.base_url = PIWEBAPI_URL
        self.auth = (PIWEBAPI_USERNAME, PIWEBAPI_PASS)

    def test_connection(self):

        """Test the connection to the PI Web API server."""

        logger.info("Testing connection to PI Web API server...")
        try:
            response = requests.get(self.base_url, auth=self.auth, verify=False)
            response.raise_for_status()
            logger.info(f"Connection successful with status code: {response.status_code}")
            return response.status_code
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection failed: {e}")
            return None

    def extract_data(self, hostname, assetServer, componentName, typeOfData, component='attributes', templateName=''):

        """Extract Timestamp and Value from selected attributes inside AF Server"""

        url=f"{PIWEBAPI_URL}/assetdatabases?path=\\\\{hostname}\\{assetServer}"
        
        # Send a GET request to the Asset Server URL
        response = requests.get(url, auth=HTTPBasicAuth(PIWEBAPI_USERNAME, PIWEBAPI_PASS), verify = False)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Parse the response as JSON
            webID= data.get("WebId") # Get the WebID of the AF Server
            
            url=f"{PIWEBAPI_URL}/{component}/search?databasewebid={webID}&query=Element:{{Template:='{templateName}'}}Name:'*{componentName}*'"

            # Send a GET request to query the attribute by name          
            response = requests.get(url, auth=HTTPBasicAuth(PIWEBAPI_USERNAME, PIWEBAPI_PASS), verify = False)
            if response.status_code == 200:
                data=response.json()
                typeOfData_url=data["Items"][0]["Links"][typeOfData] # store the URL to the type of data required
                
                # Send a GET request to the type of data URL
                response = requests.get(typeOfData_url, auth=HTTPBasicAuth(PIWEBAPI_USERNAME, PIWEBAPI_PASS), verify = False)
                if response.status_code == 200:
                    data=response.json()
                    # filter the JSON to only include timestamp and value
                    filtered_data = [{"Timestamp": item.get("Timestamp"), "Value": item.get("Value")} for item in data.get("Items", [])]
                    return filtered_data
                else:
                    print(f"Error: {response.status_code}")

            else:
                print(f"Error: {response.status_code}")    
        else:
                print(f"Error: {response.status_code}")  

"""TO DO: utilize batch request instead of requesting multiple times to the Server"""

# Utility function to save extracted data to a file
def write_data_to_file(data):

    """Writes extracted data to a JSON file."""

    with open(f"{BASE_DIR}/extracted_data8.json", "w") as f:
        json.dump(data, f, indent=4)
    logger.info("Data written to extracted_data.json successfully.")

# Main execution
if __name__ == "__main__":
    extractor = SimplePIDataExtractor()

    # Test connection
    if extractor.test_connection() == HTTP_STATUS_OK:

        # Perform data extraction. Replace the parameter accordingly
        extracted_data = extractor.extract_data(hostname='WIN-A6RTRD7NISO', assetServer='JXN', componentName='Condy Pressure', typeOfData="InterpolatedData", component='attributes', templateName='')
        
        # Save data to file
        if extracted_data:
            write_data_to_file(extracted_data)
        else:
            logger.warning("No data extracted.")
    else:
        print("Unable to connect to PI Web API Server")
        logger.error("Unable to connect to PI Web API server. Data extraction aborted.")
