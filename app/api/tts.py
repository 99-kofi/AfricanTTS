import base64
import os
import asyncio
from fastapi import APIRouter, HTTPException
from app.schemas.tts import TTSRequest, TTSResponse, TranslationRequest
from app.services.africa_tts import AfricaTTSService
from app.services.llm import LLMTranslationService

router = APIRouter()
tts_service = AfricaTTSService()
llm_service = LLMTranslationService()

@router.post("/translate")
async def translate_text(payload: TranslationRequest):
    """
    Translate English text to Asante Twi.
    Returns the translation instantly — no audio synthesis.
    """
    try:
        twi_text = await llm_service.translate(payload.english_text)
        return {"twi_text": twi_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts", response_model=TTSResponse)
async def synthesize_speech(payload: TTSRequest):
    """
    Translate English to Asante Twi and synthesize the audio.
    Returns the Twi text and a base64-encoded audio data URL (works on any platform).
    """
    try:
        twi_text = payload.twi_text

        # Step 1: Translate if twi_text not provided
        if not twi_text and payload.english_text:
            twi_text = await llm_service.translate(payload.english_text)

        if not twi_text:
            raise HTTPException(
                status_code=400,
                detail="Either 'english_text' or 'twi_text' must be provided."
            )

        # Step 2: Synthesize (Asante Twi -> Speech)
        local_temp_path = await asyncio.to_thread(
            tts_service.synthesize,
            text=twi_text,
            lang="Asante Twi",
            speaker=payload.speaker
        )

        # Step 3: Encode to base64 data URL so it works on any platform
        # (no filesystem dependency — compatible with Vercel, Railway, etc.)
        with open(local_temp_path, "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        audio_url = f"data:audio/wav;base64,{audio_b64}"

        return TTSResponse(
            audio_url=audio_url,
            twi_text=twi_text
        )
    except Exception as e:
        print(f"Synthesis Error: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"Twi TTS Failed: {str(e)}")
