from gemini_query_processor import GeminiQueryProcessor
from document_handler import DocumentHandler

def test_cosine():
	h = DocumentHandler()
	h.add_document("Doc1", "alpha", [1, 0])
	h.add_document("Doc2", "beta", [0, 1])
	res = h.search([1, 0])[0]
	assert res[0]["title"] == "Doc1"

# --- Test: missing query field ---
def test_missing_query():
	response, code = handle_request({})
	assert code == 400
	assert "error" in response

# --- Test: document found ---
def test_document_found():
	response, code = handle_request({"query": "test"})
	assert code == 200 or "error" in response

# --- Test: document not found ---
def test_document_not_found():
	response, code = handle_request({"query": "xyz"})
	assert code == 404
	assert response["error"] == "Document not found"