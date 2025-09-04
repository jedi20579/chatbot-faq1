import streamlit as st
import requests

st.title("🤖 Chatbot FAQ")
st.write("Posez vos questions, je réponds à partir de la FAQ.")

# Charger la FAQ
with open("faq.txt", "r", encoding="utf-8") as f:
    faq_content = f.read()

# Vérifier le provider
provider = st.secrets.get("PROVIDER", "hf").lower()
hf_token = st.secrets.get("HF_API_TOKEN", "")
hf_model = st.secrets.get("MODEL_HF", "google/flan-t5-small")

question = st.text_input("Votre question :")

def ask_hf(question: str) -> str:
    if not hf_token:
        return "HF_API_TOKEN manquant dans les Secrets"
    prompt = f"Réponds uniquement à partir de la FAQ suivante :\n\n{faq_content}\n\nQuestion: {question}\nRéponse:"
    url = f"https://api-inference.huggingface.co/models/{hf_model}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # Google FLAN T5 renvoie un dictionnaire simple avec 'generated_text'
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        elif isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]
        return str(data)
    except Exception as e:
        return f"Erreur HF : {e}"

if question:
    if provider == "hf":
        answer = ask_hf(question)
        st.write("💬 Réponse :", answer)
    else:
        st.write("OpenAI non configuré ou désactivé.")
