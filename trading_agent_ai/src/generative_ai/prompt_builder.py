from typing import Dict, Any

from ..core.config_loader import ConfigLoader

class PromptBuilder:
    def __init__(self, config: ConfigLoader):
        self.prompts = config.get_prompt("prompts")

    def build_signal_prompt(self, signal_details: str) -> str:
        """
        Builds a detailed prompt for the LLM to explain a signal.
        """
        base_prompt = self.prompts.get("explanation_prompt", "Explain this trading signal in simple terms: {details}")
        return base_prompt.format(details=signal_details)

    def build_chat_prompt(self, user_query: str, context: Dict[str, Any]) -> str:
        """
        Builds a prompt for the chat widget, including relevant context.
        """
        base_prompt = self.prompts.get("chat_prompt", "Context: {context}\n\nUser query: {query}\n\nAnswer:")
        return base_prompt.format(context=str(context), query=user_query)
