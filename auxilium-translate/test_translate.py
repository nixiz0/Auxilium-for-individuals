from fastapi.testclient import TestClient
from translate_api import app


client = TestClient(app)

def test_translate_french():
    lang_input = "Bonjour, comment ça va?"
    input_lang = "fr"
    response = client.post("/translate", json={"text": lang_input, "input_lang": input_lang})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    print(input_lang)
    print(f"\nLanguage Input: {lang_input}")
    print(f"Language Output (translated): {data['translated_text']}")

def test_translate_english():
    lang_input = "Hello, how are you?"
    input_lang = "en"
    response = client.post("/translate", json={"text": lang_input, "input_lang": input_lang})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    print(input_lang)
    print(f"\nLanguage Input: {lang_input}")
    print(f"Language Output (translated): {data['translated_text']}")

def test_translate_spanish():
    lang_input = "Hola, ¿cómo estás?"
    input_lang = "es"
    response = client.post("/translate", json={"text": lang_input, "input_lang": input_lang})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    print(input_lang)
    print(f"\nLanguage Input: {lang_input}")
    print(f"Language Output (translated): {data['translated_text']}")

def test_translate_german():
    lang_input = "Hallo, wie geht es Ihnen?"
    input_lang = "de"
    response = client.post("/translate", json={"text": lang_input, "input_lang": input_lang})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    print(input_lang)
    print(f"\nLanguage Input: {lang_input}")
    print(f"Language Output (translated): {data['translated_text']}")

def test_translate_japanese():
    lang_input = "こんにちは、お元気ですか？"
    input_lang = "ja"
    response = client.post("/translate", json={"text": lang_input, "input_lang": input_lang})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    print(input_lang)
    print(f"\nLanguage Input: {lang_input}")
    print(f"Language Output (translated): {data['translated_text']}")

def test_translate_italian():
    lang_input = "Ciao, come stai?"
    input_lang = "it"
    response = client.post("/translate", json={"text": lang_input, "input_lang": input_lang})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    print(input_lang)
    print(f"\nLanguage Input: {lang_input}")
    print(f"Language Output (translated): {data['translated_text']}")

def test_translate_chinese():
    lang_input = "你好，你怎么样？"
    input_lang = "zh-cn"
    response = client.post("/translate", json={"text": lang_input, "input_lang": input_lang})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    print(input_lang)
    print(f"\nLanguage Input: {lang_input}")
    print(f"Language Output (translated): {data['translated_text']}")

def test_translate_korean():
    lang_input = "안녕하세요, 어떻게 지내세요?"
    input_lang = "ko"
    response = client.post("/translate", json={"text": lang_input, "input_lang": input_lang})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    print(input_lang)
    print(f"\nLanguage Input: {lang_input}")
    print(f"Language Output (translated): {data['translated_text']}")

def test_translate_portuguese():
    lang_input = "Olá, como vai você?"
    input_lang = "pt"
    response = client.post("/translate", json={"text": lang_input, "input_lang": input_lang})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    print(input_lang)
    print(f"\nLanguage Input: {lang_input}")
    print(f"Language Output (translated): {data['translated_text']}")

def test_translate_arabic():
    lang_input = "مرحبًا ، كيف حالك؟"
    input_lang = "ar"
    response = client.post("/translate", json={"text": lang_input, "input_lang": input_lang})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    print(input_lang)
    print(f"\nLanguage Input: {lang_input}")
    print(f"Language Output (translated): {data['translated_text']}")