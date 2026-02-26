import asyncio
from mtranslate import translate

class LLMTranslationService:
    def __init__(self):
        self.persona_name = "Twi-Translator"

    async def translate(self, english_text: str) -> str:
        """
        Translate English text into Asante Twi using mtranslate (Google Translate engine).
        """
        try:
            print(f"Translating: '{english_text}'")
            # Run the synchronous translate function in a thread to keep FastAPI async
            twi_text = await asyncio.to_thread(translate, english_text, 'ak')
            
            if not twi_text or twi_text == english_text:
                print("Translation returned original or empty. Returning English.")
                return english_text

            print(f"Translated to: '{twi_text}'")
            return twi_text
            
        except Exception as e:
            print(f"Translation Error: {e}")
            return english_text
