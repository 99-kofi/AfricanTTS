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

    async def translate_to_english(self, twi_text: str) -> str:
        """
        Translate Asante Twi text into English using mtranslate.
        """
        try:
            print(f"Translating Twi: '{twi_text}'")
            english_text = await asyncio.to_thread(translate, twi_text, 'en', 'ak')
            
            if not english_text or english_text == twi_text:
                print("Translation returned original or empty. Returning original.")
                return twi_text

            print(f"Translated to English: '{english_text}'")
            return english_text
            
        except Exception as e:
            print(f"Twi-to-English Translation Error: {e}")
            return twi_text
