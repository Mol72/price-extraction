import requests
import json
from typing import Optional

class LocalLLMClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    def optimize_memory(self):
        """Configure model for memory efficiency"""
        # Use smaller context window
        self.default_options = {
            "num_ctx": 2048,  # Reduce from default 4096
            "num_batch": 512,  # Smaller batch size
            "num_gpu_layers": 0  # Use CPU only if needed
        }
    def generate(self, prompt: str, model: str = "gemma3:4b", 
                temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Generate text using local LLM"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Local LLM request failed: {e}")

# Example usage
if __name__ == "__main__":
    client = LocalLLMClient()

    document = """
    Artificial intelligence has transformed software development through 
    automated code generation, intelligent debugging, and enhanced testing 
    capabilities. Modern AI tools can analyze codebases, suggest improvements, 
    and even write entire functions based on natural language descriptions.
    """

    prompt = f"Extract the prices of Iphones in this paragraph:\n\n{document}"
    
    summary = client.generate(prompt, temperature=0.3)
    print(f"Summary: {summary}")