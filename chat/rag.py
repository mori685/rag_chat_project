import openai
from sentence_transformers import SentenceTransformer
import faiss

class RAG:
    def __init__(self, api_key):
        self.encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.index = None
        self.documents = []
        openai.api_key = api_key

    def add_documents(self, documents):
        self.documents.extend(documents)
        embeddings = self.encoder.encode(documents)
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def generate_response(self, query):
        query_embedding = self.encoder.encode([query])
        _, I = self.index.search(query_embedding, k=3)
        context = " ".join([self.documents[i] for i in I[0]])
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Use the following context to answer the user's question."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        
        return response.choices[0].message['content'].strip()