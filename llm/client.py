import ollama

try:
    response = ollama.generate(
        model='qwen3.5:4b',
        prompt='Hey, how are you?'
    )
    print(response.response)
except ConnectionError as e:
    print(f"Failed to connect to Ollama: {e}")
    print("\nPossible fixes:")
    print("1. Ensure Ollama is installed and running.")
    print("2. Check that Ollama is accessible at the expected URL.")
except Exception as e:
    print(f"An error occurred: {e}")
