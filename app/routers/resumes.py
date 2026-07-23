import io
from datetime import datetime

from typing import Annotated, cast
import asyncio

import pdfplumber
from fastapi import APIRouter, Form, UploadFile, File, HTTPException

from app.models.Resumes import Resumes
from app.schemas.resumes_request import ResumesRequest
from app.services.resumes_service import extract_text_from_pdf, extract_skills_from_resume

resumes_router = APIRouter()




@resumes_router.post("/resumes", response_model=ResumesRequest)
async def store_resume(role_name: Annotated[str, Form()], file: Annotated[UploadFile, File()]):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type, must be a PDF")

    try:
        file_name = cast(str, file.filename)
        file_content = await file.read()
        text_content = await asyncio.to_thread(extract_text_from_pdf, file_content)
        ai_parsed_resume = await extract_skills_from_resume(text_content)

        existing_resume = await Resumes.find_one(Resumes.role_name == role_name)

        if existing_resume:
            existing_resume.raw_text = text_content
            existing_resume.uploaded_at = datetime.now()
            existing_resume.file_name = file_name
            existing_resume.experience_summary = ai_parsed_resume.experience_summary
            await existing_resume.save()
            return existing_resume
        else:
            resumes = Resumes(raw_text=text_content, role_name=role_name, uploaded_at=datetime.now(), skills=ai_parsed_resume.skills,
                              file_name=file_name, experience_summary=ai_parsed_resume.experience_summary)
            await resumes.insert()
            return resumes

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
