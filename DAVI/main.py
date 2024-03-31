import openai
from dotenv import load_dotenv
import os
import pyttsx3
import speech_recognition as sr

# Carrega as variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("OPEN_AI_KEY")

# Função para capturar a frase do microfone
def ouvir_microfone():
    microfone = sr.Recognizer()

    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)

        print("Estou ouvindo: ")

        audio = microfone.listen(source)

    try:
        frase = microfone.recognize_google(audio, language='pt-BR')
        print("Você disse: " + frase)
        return frase
    except sr.UnknownValueError:
        print("Não entendi")
        return None

# Função para interagir com a API OpenAI
def ask_gpt(mensagens, frase):
    mensagens = [mensagens[0]] + mensagens[-10:] + [{"role": "user", "content": frase}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=mensagens,
        max_tokens=500,
        temperature=1
    )
    return response['choices'][0]['message']['content']

# Função principal
def main():
    # Define as variáveis
    nome = "Unknown"
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # Define a voz desejada

    # Mensagem inicial
    mensagens = [{"role": "system", "content": f"Seu nome é {nome} você é uma inteligencia artificial feita para ajudar deficientes visuais. Por tanto responderá dúvidas e ajudará no que for possivel."},]

    while True:
        # Captura a frase do usuário
        frase = ouvir_microfone()

        # Se a frase for válida
        if frase is not None:
            # Adiciona a mensagem do usuário à lista
            mensagens.append({"role": "user", "content": frase})

            # Envia a frase para a API OpenAI e recebe a resposta
            resposta = ask_gpt(mensagens, frase)

            # Adiciona a resposta do sistema à lista
            mensagens.append({"role": "system", "content": resposta})

            # Exibe a resposta na tela e reproduz em voz alta
            print(f"{nome}:", resposta)
            engine.say(resposta)
            engine.runAndWait()

# Executa a função principal
if __name__ == "__main__":
    main()