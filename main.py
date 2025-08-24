from document_handler import DocumentHandler 
from constants import DOC_CONTENT, QUERY 
from gemini_query_processor import GeminiQueryProcessor 

""""

Main program file that handles user requests

"""

def handle_request(request_data) -> str:
    processor = GeminiQueryProcessor()
    handler = DocumentHandler()

    # Add some test documents
    handler.add_document({"title": "Doc1", "content": "This is a test document."})
    handler.add_document({"title": "Doc2", "content": "Another document content."})


    query = request_data[QUERY]
    doc = handler.search_documents(query)
    if doc:
        result = processor.query_model(doc[DOC_CONTENT])
        return result
    else:
        return {"error": "Document not found"}

if __name__ == "__main__":
	handle_request(request_data)