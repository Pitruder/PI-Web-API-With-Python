# PI-Web-API-With-Python
A repository to store python scripts used to extract data inside PI Data Archive and PI AF server.

This tool enables data extraction from a PI Web API server, specifically retrieving timestamp and value pairs for specified attributes in an AF (Asset Framework) server. It includes logging and error handling to monitor and troubleshoot connections and data retrieval.

*Features*-

Environment-based Configuration: Reads PI Web API URL, username, password, and log level from environment variables (.env file).
Logging: Logs application events to app.log with configurable levels, file rotation at 5MB.
Connection Testing: Verifies server connection before data extraction.
Data Extraction: Retrieves interpolated or recorded data by specifying hostname, asset server, component name, and type of data.
File Output: Saves extracted data to extracted_data.json in JSON format.

*Requirements*-

requests, loguru, and python-dotenv Python packages.

*Setup*-

Environment Variables: Configure .env file with PI Web API connection details:

PIWEBAPI_LOCAL=<PI Web API URL>

PIUSERNAME_LOCAL=<Username>

PIPASSWORD_LOCAL=<Password>

LOG_LEVEL=INFO

Install Dependencies:
pip install requests loguru python-dotenv

*Usage*-

python Simple_PI_Web_API_Extractor.py

It will:

Test the connection to the server.
Extract the specified data.
Save it to extracted_data.json.

Example Function Call:

extracted_data = extractor.extract_data(
    hostname='WIN-K9RTRD7HERO', 
    assetServer='HJK', 
    componentName='Condy Pressure', 
    typeOfData="InterpolatedData", 
    component='attributes', 
    templateName=''
)

Logging and Errors: Logs events and errors to app.log in the logs folder.
