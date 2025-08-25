from document_handler import DocumentHandler 
from constants import DOC_CONTENT, QUERY 
from gemini_query_processor import GeminiQueryProcessor
from typing import Tuple, Dict

""""

Main program file that handles user requests

"""

def handle_request(request_data) -> Tuple[Dict, int]:
    processor = GeminiQueryProcessor()
    handler = DocumentHandler()

    # Add some test documents
    handler.add_document({"title": "Doc1", "content": "This is a test document."})
    handler.add_document({"title": "Doc2", "content": "Another document content."})


    # --- Extract query from request (validation) ---
    if "query" not in request_data:
        return {"error": "Missing 'query' in request"}

    query = request_data[QUERY]
    doc = handler.search_documents(query)

    if doc:
        result = processor.query_model(doc[DOC_CONTENT])
        return result, 200
    else:
        return {"error": "Document not found"}, 404

if __name__ == "__main__":
    request = {"query": "test"}
    response, code = handle_request(request)
    print("Response:", response)