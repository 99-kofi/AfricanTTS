import base64
import os
import asyncio
from gtts import gTTS
import tempfile

class EnglishTTSService:
    async def synthesize(self, text: str) -> str:
        """
        Synthesize English speech using gTTS and return a base64 data URL.
        """
        try:
            print(f"Synthesizing English: '{text}'")
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_path = fp.name
            
            # Run gTTS in a thread to keep FastAPI async
            def _save_gtts():
                tts = gTTS(text=text, lang='en')
                tts.save(temp_path)
            
            await asyncio.to_thread(_save_gtts)
            
            # Read and encode to base64
            with open(temp_path, "rb") as f:
                audio_bytes = f.read()
            
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
            audio_url = f"data:audio/mp3;base64,{audio_b64}"
            
            # Clean up temp file
            os.remove(temp_path)
            
            return audio_url
            
        except Exception as e:
            print(f"English TTS Error: {e}")
            raise e
