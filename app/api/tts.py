import base64
import os
import asyncio
from fastapi import APIRouter, HTTPException
from app.schemas.tts import TTSRequest, TTSResponse, TranslationRequest, TwiToEnglishRequest, TwiToEnglishResponse
from app.services.africa_tts import AfricaTTSService
from app.services.llm import LLMTranslationService
from app.services.english_tts import EnglishTTSService

router = APIRouter()
tts_service = AfricaTTSService()
llm_service = LLMTranslationService()
english_tts_service = EnglishTTSService()

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(payload: TranslationRequest):
    """
    Translate English text to Asante Twi.
    """
    try:
        twi_text = await llm_service.translate(payload.english_text)
        return TranslationResponse(translated_text=twi_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate-twi", response_model=TranslationResponse)
async def translate_twi_short(payload: TwiToEnglishRequest):
    """
    Translate Asante Twi text to English.
    """
    try:
        english_text = await llm_service.translate_to_english(payload.twi_text)
        return TranslationResponse(translated_text=english_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts", response_model=TTSResponse)
async def synthesize_speech(payload: TTSRequest):
    """
    Translate English to Asante Twi and synthesize the audio.
    """
    try:
        twi_text = payload.twi_text

        if not twi_text and payload.english_text:
            twi_text = await llm_service.translate(payload.english_text)

        if not twi_text:
            raise HTTPException(
                status_code=400,
                detail="Either 'english_text' or 'twi_text' must be provided."
            )

        local_temp_path = await asyncio.to_thread(
            tts_service.synthesize,
            text=twi_text,
            lang="Asante Twi",
            speaker=payload.speaker
        )

        with open(local_temp_path, "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        audio_url = f"data:audio/wav;base64,{audio_b64}"

        if os.path.exists(local_temp_path):
            os.remove(local_temp_path)

        return TTSResponse(
            audio_url=audio_url,
            twi_text=twi_text
        )
    except Exception as e:
        print(f"Asante Twi Synthesis Error: {e}")
        raise HTTPException(status_code=500, detail=f"Twi TTS Failed: {str(e)}")

@router.post("/tts-english", response_model=TwiToEnglishResponse)
async def synthesize_english_speech(payload: TwiToEnglishRequest):
    """
    Translate Twi to English and synthesize English speech.
    """
    try:
        english_text = await llm_service.translate_to_english(payload.twi_text)
        
        audio_url = None
        if payload.include_audio:
            audio_url = await english_tts_service.synthesize(english_text)
            
        return TwiToEnglishResponse(
            english_text=english_text,
            audio_url=audio_url
        )
    except Exception as e:
        print(f"English Synthesis Error: {e}")
        raise HTTPException(status_code=500, detail=f"English TTS Failed: {str(e)}")
