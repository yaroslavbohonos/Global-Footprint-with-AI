from google import genai
import json

# Use your Google AI Studio API key here directly
GEMINI_API_KEY = "AIzaSyC0wZuu3zu9ulOnYdudLrVMeM7zVEaux8Y"
# Create the client with your API key
client = genai.Client(api_key=GEMINI_API_KEY)

def extract_company_esg(company_name):
    """
    Extract structured ESG/footprint data using Gemini API.
    Returns a dictionary.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Return ESG data for {company_name} in JSON format with only the format, no extra information(all single numbers either scores from 0 to 100 but don't expand it further):
        Environmental , Social, Governance,
        TransparencyIndex, Scope1, Scope2, Scope3,
        SustainabilityInvestmentRatio, DataConfidence
        """
    )
    print(response.text)
    extract_company_report(company_name)
    return response.text

def extract_company_report(company_name):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Return a report for global footprint impact of the {company_name}. 
        The report must be very consice and written in plain English. 
        Limit the message to two paragraphs
        Include and referece the data from the ESG data too.
        """
    )
    print(response.text)