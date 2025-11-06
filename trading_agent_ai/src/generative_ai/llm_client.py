import ollama
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, model: str = 'phi3'):
        self.model = model
        try:
            # Check if the Ollama server is running
            ollama.list()
        except Exception as e:
            logger.error("Ollama server not running. Please start it to use the GenAI features.")
            raise ConnectionError("Ollama server not available.") from e

    def get_explanation(self, prompt: str) -> str:
        """
        Gets an explanation from the local LLM.
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"Error communicating with Ollama: {e}")
            return "Error: Could not get explanation from LLM."
