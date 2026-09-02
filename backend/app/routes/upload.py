"""
Upload Route — CSV File Ingestion
----------------------------------
Flow:
  1. Client sends a POST /upload request with a CSV file (multipart/form-data)
  2. FastAPI's UploadFile streams the file into memory without blocking
  3. We validate the file extension is .csv before touching disk
  4. File is written to maritime-poc/uploads/ using pathlib
  5. JSON response confirms filename, size, and status

Why UploadFile?
  - Handles large files efficiently via streaming (no full memory load)
  - Gives access to filename, content_type, and async read()
  - Native FastAPI support — shows up cleanly in Swagger /docs

Where files are stored:
  - All uploads land in: maritime-poc/uploads/
  - Path is resolved relative to this file's location so it works
    regardless of where uvicorn is launched from
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path

router = APIRouter(prefix="/upload", tags=["Upload"])

# Resolve uploads/ relative to project root (3 levels up from this file)
UPLOAD_DIR = Path(__file__).resolve().parents[3] / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)  # safety: create if somehow missing


@router.post("/", summary="Upload a CSV dataset file")
async def upload_csv(file: UploadFile = File(...)):
    # Validate file extension — only .csv allowed
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.filename}'. Only .csv files are accepted."
        )

    destination = UPLOAD_DIR / file.filename

    # Read and write file contents to disk
    contents = await file.read()
    destination.write_bytes(contents)

    return {
        "status": "success",
        "filename": file.filename,
        "size_bytes": len(contents),
        "saved_to": str(destination)
    }
