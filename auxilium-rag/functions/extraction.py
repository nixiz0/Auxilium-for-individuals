from langchain_community.document_loaders  import TextLoader, PyPDFLoader, JSONLoader, UnstructuredFileLoader


def extract_text(file_paths):
    documents = []
    for path in file_paths:
        if path.endswith(".txt"):
            loader = TextLoader(path, encoding="utf-8")
        elif path.endswith(".json"):
            loader = JSONLoader(path, encoding="utf-8")
        elif path.endswith(".pdf"):
            loader = PyPDFLoader(path)
        else:
            loader = UnstructuredFileLoader(path)
        documents.extend(loader.load())
    return documents