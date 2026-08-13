import ollama
from typing import List, Dict, Generator
from dotenv import load_dotenv
import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import load_settings


load_dotenv(override=True)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


class OllamaLuna:
    def __init__(self, model:str = None , host: str = None):
        settings = load_settings()
        self.host = settings.ollama_host
        self.model = settings.models.modes[settings.models.default_mode].model
        if not self.host or not self.model:
            raise ValueError("OLLAMA_HOST and OLLAMA_MODEL must be set in .env file")
        self.client = ollama.Client(host=self.host)
        
    def stream_chat(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """Streams responses from the Ollama model in chunks."""
        try:
            response = self.client.chat(
                model = self.model,
                messages = messages,
                stream = True,
                think = False
            )

            for chunk in response:
                yield chunk.message.content
        except Exception as e:
            yield f"Error: {e}"

def continuous_chat():
    llm = OllamaLuna()
    messages = [{"role": "system","content":"You are Luna, a highly capable, friendly, and concise personal AI assistant. "
        "When asked who you are or what your name is, always identify yourself as Luna."}]

    print("Chatbot initialized! Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit' ,'quit']:
            print("Goodbye!")
            break
        
        messages.append({"role": "user", "content":user_input})

        print("\nLuna: ", end="", flush=True)
        assistant_reply = ""

        for chunk in llm.stream_chat(messages):
            print(chunk, end="", flush=True)
            assistant_reply += chunk

        print("\n")
        messages.append({"role": "assistant", "content": assistant_reply})
        
if __name__ == "__main__":
    continuous_chat()
   