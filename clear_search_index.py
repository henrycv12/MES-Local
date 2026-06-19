"""Delete Azure AI Search index (clean slate). The index will be recreated by ingest_excel.py."""
import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

load_dotenv()

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY", "")
SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX", "work-orders")

if not (SEARCH_ENDPOINT and SEARCH_KEY):
    raise RuntimeError("Azure Search credentials missing. Set AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_KEY in .env")

admin_client = SearchIndexClient(
    endpoint=SEARCH_ENDPOINT,
    credential=AzureKeyCredential(SEARCH_KEY),
)

# Check if index exists and delete it
try:
    admin_client.get_index(SEARCH_INDEX)
    print(f"Deleting index '{SEARCH_INDEX}'...")
    admin_client.delete_index(SEARCH_INDEX)
    print(f"Index '{SEARCH_INDEX}' deleted successfully.")
    print(f"Run 'python ingest_excel.py' to recreate the index with your new data.")
except Exception as e:
    print(f"Index '{SEARCH_INDEX}' does not exist or could not be deleted: {e}")
    print(f"Run 'python ingest_excel.py' to create the index with your new data.")
