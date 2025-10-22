# Online Chat for Kids

| Sekcja | Opis |
|--------|------|
| **Opis** | Webowa aplikacja edukacyjna dla dzieci, pozwala zadawać pytania i otrzymywać bezpieczne odpowiedzi od AI. Wspiera transkrypcję audio i TTS. |
| **Funkcjonalności** | - Chat z LLM (Gemini 1.5 Flash) z filtrem treści dla dzieci<br>- Transkrypcja MP3 na tekst (Whisper)<br>- Konwersja odpowiedzi na mowę (TTS, gTTS)<br>- Frontend HTML/JS |
| **Instalacja** | 1. `git clone <repo>`<br>2. `python -m venv venv`<br>3. Aktywacja venv (`venv\Scripts\activate` lub `source venv/bin/activate`)<br>4. `pip install -r requirements.txt`<br>5. `.env` z `GOOGLE_API_KEY=twój_klucz_API` |
| **Struktura** | - `app/` – backend i moduły<br>- `frontend/` – HTML, JS<br>- `transcribe.py` – transkrypcja audio<br>- `utils.py` – wywołanie LLM<br>- `.env` – klucz API<br>- `requirements.txt` – zależności |
| **Przykład użycia** | - `call_llm("Why is the sky blue?")` – odpowiada AI<br>- `transcribe_audio("example.mp3")` – zwraca tekst z audio |
| **Bezpieczeństwo** | System filtruje nieodpowiednie treści i zapewnia odpowiedzi przyjazne dzieciom. |
