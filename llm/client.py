import ollama

try:
    response = ollama.generate(
        model='qwen3.5:4b',
        prompt='Hey, how are you?'
    )
    print(response.response)
except ollama.ModelNotFoundError:
    print("The specified model 'qwen3.5:4b' is not found.")
except Exception as e:
    print(f"An error occurred: {e}")
    print("\nPossible fixes:")
    print("1. Ensure Ollama is installed and running.")
    print("2. Check installed models using 'ollama list' in terminal.")
