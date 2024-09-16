import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from deep_translator import GoogleTranslator
import torch

# Function to load the GPT-2 model and tokenizer
@st.cache_resource
def load_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        model = AutoModelForCausalLM.from_pretrained("gpt2")
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

# Function to generate text from the model
def generate_text(model, tokenizer, prompt, max_length=200):
    inputs = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(inputs, max_length=max_length, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function to translate text to English
def translate_to_english(text, source_lang='auto'):
    try:
        return GoogleTranslator(source=source_lang, target='en').translate(text)
    except Exception as e:
        st.error(f"Translation to English failed: {e}")
        return text

# Function to translate text back to the original language
def translate_to_original(text, target_lang='auto'):
    try:
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except Exception as e:
        st.error(f"Translation to original language failed: {e}")
        return text

# Main Streamlit app
def main():
    st.title("Gynecology AI Chatbot")

    # Load the model and tokenizer
    model, tokenizer = load_model()

    if model is None or tokenizer is None:
        st.error("Failed to load the model.")
        return

    # User input for the chatbot
    user_input = st.text_area("Ask your question about gynecology or obstetrics:", "", height=150)

    # If the user provides input, detect the language and translate if needed
    if user_input:
        # Detect the input language automatically
        detected_lang = GoogleTranslator(source='auto', target='en').detect(user_input)
        st.write(f"Detected language: {detected_lang}")

        # Translate input to English
        translated_input = translate_to_english(user_input, source_lang=detected_lang)

        # Generate response
        with st.spinner("Generating response..."):
            response = generate_text(model, tokenizer, translated_input)

        # Translate response back to the original language
        translated_response = translate_to_original(response, target_lang=detected_lang)

        # Display the response
        st.write(translated_response)

if __name__ == "__main__":
    main()
