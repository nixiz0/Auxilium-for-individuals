import os
from tempfile import NamedTemporaryFile
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from CONFIG import *
from functions.check_pull_model import check_and_pull_model
from functions.load_collections import load_existing_collections
from functions.extraction import extract_text


# ----[Initialize]----
collections = {}
document_store = {}
app = FastAPI()
check_and_pull_model(MODEL_RESPONSE)
check_and_pull_model(MODEL_VECTOR)
load_existing_collections(collections, document_store)  # Load existing collections at startup


# ----[Manage Vectorstore]----
def create_vectorstore(collection_name):
    """
    Create a new vector store with the given collection name.
    
    Parameters:
    collection_name (str): The name of the collection to create.
    
    Raises:
    HTTPException: If the collection already exists (status code 400).
    """
    if collection_name in collections:
        raise HTTPException(status_code=400, detail="Collection already exists")
    
    collection_path = os.path.join(VECTORSTORE_DIR, collection_name)
    
    embeddings = OllamaEmbeddings(base_url=OLLAMA_API, model=MODEL_VECTOR)
    
    vector_store = FAISS.from_texts(
        texts=[""],  # Initialization with empty text
        embedding=embeddings,
        metadatas=[{"source": "initialization"}]
    )
    
    vector_store.save_local(collection_path)
    collections[collection_name] = vector_store
    document_store[collection_name] = {}

def delete_vectorstore(collection_name):
    """
    Delete the vector store with the given collection name.
    
    Parameters:
    collection_name (str): The name of the collection to delete.
    
    Raises:
    HTTPException: If the collection is not found (status code 404).
    """
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")
    collection_path = os.path.join(VECTORSTORE_DIR, collection_name)
    if os.path.exists(collection_path):
        import shutil
        shutil.rmtree(collection_path)
    del collections[collection_name]
    del document_store[collection_name]

def rename_vectorstore(old_name, new_name):
    """
    Rename an existing vector store from old_name to new_name.
    
    Parameters:
    old_name (str): The current name of the collection.
    new_name (str): The new name for the collection.
    
    Raises:
    HTTPException: If the old collection name is not found (status code 404) or the new name already exists (status code 400).
    """
    if old_name not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")
    if new_name in collections:
        raise HTTPException(status_code=400, detail="New collection name already exists")
    old_path = os.path.join(VECTORSTORE_DIR, old_name)
    new_path = os.path.join(VECTORSTORE_DIR, new_name)
    os.rename(old_path, new_path)
    collections[new_name] = collections.pop(old_name)
    document_store[new_name] = document_store.pop(old_name)


# ----[Routes]----
class CollectionRequest(BaseModel):
    collection_name: str

class QueryRequest(BaseModel):
    collection_name: str
    query: str
    history: List[str]

class RenameRequest(BaseModel):
    old_name: str
    new_name: str

class DeleteDocumentRequest(BaseModel):
    collection_name: str
    document_name: str

@app.get("/")
def root():
    """
    Root endpoint that returns a welcome message.

    Returns:
    dict: A dictionary with a welcome message.
    """
    return {"message": "Welcome to RAG API"}

@app.post("/create_collection/")
def create_collection(request: CollectionRequest):
    """
    Create a new vector store collection.

    Parameters:
    request (CollectionRequest): The request containing the collection name.

    Returns:
    dict: A dictionary with a success message.
    """
    create_vectorstore(request.collection_name)
    return {"message": f"Collection {request.collection_name} created successfully"}

@app.delete("/delete_collection/")
def delete_collection(request: CollectionRequest):
    """
    Delete an existing vector store collection.

    Parameters:
    request (CollectionRequest): The request containing the collection name.

    Returns:
    dict: A dictionary with a success message.
    """
    delete_vectorstore(request.collection_name)
    return {"message": f"Collection {request.collection_name} deleted successfully"}

@app.put("/rename_collection/")
def rename_collection(request: RenameRequest):
    """
    Rename an existing vector store collection.

    Parameters:
    request (RenameRequest): The request containing the old and new collection names.

    Returns:
    dict: A dictionary with a success message.
    """
    rename_vectorstore(request.old_name, request.new_name)
    return {"message": f"Collection {request.old_name} renamed to {request.new_name}"}

@app.get("/list_collections/")
def list_collections():
    """
    List all existing vector store collections.

    Returns:
    dict: A dictionary with the list of collection names.
    """
    return {"collections": list(collections.keys())}

@app.post("/upload_document/")
async def upload_document(collection_name: str, file: UploadFile = File(...)):
    """
    Upload a document to a vector store collection.

    Parameters:
    collection_name (str): The name of the collection to upload the document to.
    file (UploadFile): The file to upload.

    Raises:
    HTTPException: If the collection is not found (status code 404) or an error occurs during processing (status code 500).

    Returns:
    dict: A dictionary with a success message.
    """
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")

    try:
        content = await file.read()
        ext = os.path.splitext(file.filename)[-1].lower()
        if not ext:  
            ext = ".txt"

        with NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        documents = extract_text([temp_file_path])
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNCK_SIZE, chunk_overlap=CHUNCK_OVERLAP)
        texts = text_splitter.split_documents(documents)

        collections[collection_name].add_texts(
            [t.page_content for t in texts], 
            metadatas=[{"source": file.filename} for _ in texts]
        )

        if file.filename not in document_store[collection_name]:
            document_store[collection_name][file.filename] = []
        document_store[collection_name][file.filename].extend(texts)

        collection_path = os.path.join(VECTORSTORE_DIR, collection_name)
        collections[collection_name].save_local(collection_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    finally:
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

    return {"message": f"Document {file.filename} uploaded successfully to {collection_name}"}

@app.post("/query_collection/")
def query_collection(request: QueryRequest):
    """
    Query a vector store collection.

    Parameters:
    request (QueryRequest): The request containing the collection name and query.

    Raises:
    HTTPException: If the collection is not found (status code 404).

    Returns:
    dict: A dictionary with the result and source documents.
    """
    if request.collection_name not in collections:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    llm = OllamaLLM(model=MODEL_RESPONSE, base_url=OLLAMA_API)
    retriever = collections[request.collection_name].as_retriever(search_type="similarity", search_kwargs={"k": K_NUMBER_DOC_RETRIEVE})

    compressor = LLMChainExtractor.from_llm(llm)
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=compression_retriever, 
        return_source_documents=True
    )

    if request.history:
        context = "\n".join(request.history)
        query_with_context = f"{context}\n\n{request.query}"
    else:
        query_with_context = request.query

    result = qa_chain.invoke({"query": query_with_context})
    source_documents = [doc.page_content for doc in result.get("source_documents", [])]

    return {
        "source_documents": source_documents,
        "result": result["result"],
    }