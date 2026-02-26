from gradio_client import Client
from app.config import settings

class AfricaTTSService:
    def __init__(self):
        self.client = None

    def _get_client(self):
        if self.client is None:
            self.client = Client(settings.GRADIO_SPACE)
        return self.client

    def synthesize(self, text: str, lang: str, speaker: str):
        """
        Synthesize speech using the Africa-TTS Gradio space.
        """
        client = self._get_client()
        result = client.predict(
            text=text,
            lang=lang,
            speaker=speaker,
            api_name="/synthesize"
        )
        return result
