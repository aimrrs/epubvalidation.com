from fastapi import FastAPI, UploadFile, File, HTTPException, status, BackgroundTasks
from pathlib import Path
import shutil
import subprocess

app = FastAPI()

STORAGE = Path("user-uploads")
STORAGE.mkdir(parents=True, exist_ok=True)

CHECKER = Path("epubcheck-5.3.0/epubcheck.jar")

def validateEpubFile (file_path: Path):
    command = ["java", "-jar", str(CHECKER), str(file_path)]

    try:
        process = subprocess.run(command, capture_output=True, text=True, check=False)
        is_valid = (process.returncode == 0)
        output = process.stdout + process.stderr

        return {"is_valid": is_valid,
                "logs": output}
    
    except Exception as e:
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Validation Execution Failed."
        )


@app.post("/validate-epubfile", status_code=status.HTTP_200_OK, tags=["FILE UPLOAD & VALIDATION"])
def getFileAndValidation (inputFile: UploadFile = File(...), background_task: BackgroundTasks = BackgroundTasks()):
    
    file_name = Path(inputFile.filename).name
    file_extension = Path(file_name).suffix.lower()

    # Check file for .epub
    if file_extension != ".epub":
        raise HTTPException (
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported File Type. Only '.epub' File is allowed."
        )

    # Save file.
    file_location = STORAGE / file_name
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(inputFile.file, buffer)
    finally:
        inputFile.file.close()    

    validation_result = validateEpubFile(file_location)

    background_task.add_task(file_location.unlink, missing_ok=True)

    return {"message": "File Processed and Deleted.",
            "file_name": file_name,
            "is_valid": validation_result["is_valid"],
            "validation_logs": validation_result["logs"]}


# aimrrs