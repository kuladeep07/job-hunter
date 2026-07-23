import io

import pdfplumber

from app.core.configs.ai_prompts import RESUME_EXTRACT_PROMPT
from app.schemas.resumes_request import AIResumeParserRequest
from app.services.ai_communicator import aichat_structured_response


def extract_text_from_pdf(file_content: bytes):
    extracted_text = ""

    try:
        with pdfplumber.open(io.BytesIO(file_content)) as file:
            for page in file.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

        return extracted_text
    except Exception as e:
        raise RuntimeError(f"Error processing PDF: {str(e)}")


async def extract_skills_from_resume(text_content: str) -> AIResumeParserRequest | None:

    prompt = RESUME_EXTRACT_PROMPT + "\n" + text_content
    interaction = await aichat_structured_response(prompt, AIResumeParserRequest)

    return interaction
