from pydantic import BaseModel, Field
from typing import Optional, Literal

class TranslationRequest(BaseModel):
    english_text: str = Field(..., description="The English text to translate.")

class TTSRequest(BaseModel):
    english_text: Optional[str] = Field(None, description="The English text to translate and synthesize.")
    twi_text: Optional[str] = Field(None, description="Direct Twi text to synthesize (skips translation).")
    speaker: Literal["Female", "Male (Low)", "Male (High)"] = Field("Female", description="The speaker voice.")

class TTSResponse(BaseModel):
    audio_url: str = Field(..., description="Data URL (base64) or static path to the generated audio.")
    twi_text: str = Field(..., description="The translated Asante Twi text.")

class TwiToEnglishRequest(BaseModel):
    twi_text: str = Field(..., description="The Twi text to translate and/or synthesize.")
    include_audio: bool = Field(True, description="Whether to include TTS audio.")

class TwiToEnglishResponse(BaseModel):
    english_text: str = Field(..., description="The translated English text.")
    audio_url: Optional[str] = Field(None, description="Data URL (base64) for English TTS if requested.")
