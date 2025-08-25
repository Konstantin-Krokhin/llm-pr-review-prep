from constants import DOC_CONTENT 
from gemini_query_processor import GeminiQueryProcessor 

"""

DocumentHandler class is used for appending the company documents and searching 
inside the using the query from the user based on the content inside each document.
Further will be extended with metadata search to improve search time.

"""


class DocumentHandler:
    def __init__(self) -> None:
        self.documents = []

    def add_document(self, doc) -> None:
        # doc is a dictionary with 'title' and 'content'
        self.documents.append(doc)

    def search_documents(self, query) -> dict | None:
        processor = GeminiQueryProcessor()
        # Returns the first document that contains the query string
        if not self.documents:
            return None
        # Check query against the bad input
        processor.query_validation(query)
        # Here I need to check query for non-malicious code, inputs
        for doc in self.documents:
            if query in doc[DOC_CONTENT]:
                return doc
        return None