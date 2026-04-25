# EPUB Validation Service API

A FastAPI REST API for uploading and validating EPUB files using epubcheck.

## Endpoint

### POST `/validate-epubfile`

Uploads and validates an EPUB file.

**Request:**
- Content-Type: `multipart/form-data`
- Parameter: `inputFile` (File, required, `.epub` extension)

**Example:**
```bash
curl -X POST "http://localhost:8000/validate-epubfile" \
  -F "inputFile=@document.epub"
```

## Responses

### Success (200)
```json
{
  "message": "File Processed and Deleted.",
  "file_name": "document.epub",
  "is_valid": true,
  "validation_logs": "Validating against EPUB 3.3 rules.\nNo errors or warnings detected."
}
```

### Invalid EPUB (200)
```json
{
  "message": "File Processed and Deleted.",
  "file_name": "document.epub",
  "is_valid": false,
  "validation_logs": "ERROR: Missing required file: mimetype"
}
```

### Error (415)
```json
{
  "detail": "Unsupported File Type. Only '.epub' File is allowed."
}
```

### Error (500)
```json
{
  "detail": "Validation Execution Failed."
}
```

## Usage

**Python:**
```python
import requests
with open('book.epub', 'rb') as f:
    response = requests.post('http://localhost:8000/validate-epubfile', files={'inputFile': f})
    print(response.json())
```

**JavaScript:**
```javascript
const formData = new FormData();
formData.append('inputFile', fileInput.files[0]);
fetch('http://localhost:8000/validate-epubfile', { method: 'POST', body: formData })
  .then(res => res.json())
  .then(data => console.log(data));
```

**Postman:**
- POST to `http://localhost:8000/validate-epubfile`
- Body → form-data
- Key: `inputFile` (File type)

## Key Points

- Accepts `.epub` files only
- Returns validation status and logs
- Files are automatically deleted after validation
- Uses epubcheck 5.3.0 for validation
- Interactive docs at `/docs` (Swagger) or `/redoc`
