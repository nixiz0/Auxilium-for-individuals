import requests
from CONFIG import RAG_API_TEST


def test_create_collection(collection_name):
    response = requests.post(f"{RAG_API_TEST}/create_collection/", data={"collection_name": collection_name})
    print(response.json())

def test_list_collections():
    response = requests.get(f"{RAG_API_TEST}/list_collections/")
    print(response.json())

def test_upload_document(collection_name, file_path):
    with open(file_path, "rb") as file:
        response = requests.post(
            f"{RAG_API_TEST}/upload_document/",
            files={"file": file},
            data={"collection_name": collection_name}
        )
    print(response.json())

def test_query_collection(collection_name, query):
    response = requests.post(
        f"{RAG_API_TEST}/query_collection/",
        data={"collection_name": collection_name, "query": query}
    )
    print(response.json())

def test_rename_collection(old_name, new_name):
    response = requests.put(
        f"{RAG_API_TEST}/rename_collection/",
        data={"old_name": old_name, "new_name": new_name}
    )
    print(response.json())

def test_delete_document(collection_name, document_name):
    response = requests.delete(
        f"{RAG_API_TEST}/delete_document/",
        data={"collection_name": collection_name, "document_name": document_name}
    )
    print(response.json())

def test_delete_collection(collection_name):
    response = requests.delete(
        f"{RAG_API_TEST}/delete_collection/",
        data={"collection_name": collection_name}
    )
    print(response.json())


if __name__ == "__main__":
    test_create_collection("test_collection")
    test_list_collections()
    test_upload_document("test_collection", "data_test/example.txt")
    test_query_collection("test_collection", "L'aéronautique comporte combien de classes d'engins ?")
    test_rename_collection("test_collection", "renamed_collection")
    test_delete_document("renamed_collection", "data_test/example.txt")
    test_delete_collection("renamed_collection")