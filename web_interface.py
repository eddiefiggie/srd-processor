"""
FastAPI web interface for SRD processing.
Provides REST API and web UI for the SRD processor.
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import json
from pathlib import Path
import uuid
from datetime import datetime

app = FastAPI(title="D&D SRD Processor API", version="1.0.0")

# Data models
class ProcessingRequest(BaseModel):
    config_profile: str = "default"
    enable_ai_cleanup: bool = True
    chunk_min_words: int = 200
    chunk_max_words: int = 500

class ProcessingStatus(BaseModel):
    job_id: str
    status: str  # "queued", "processing", "completed", "failed"
    progress: float
    current_step: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

# In-memory job tracking (use Redis/database in production)
jobs: Dict[str, ProcessingStatus] = {}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main web interface."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>D&D SRD Processor</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .upload-area { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
            .status { padding: 10px; margin: 10px 0; border-radius: 4px; }
            .processing { background-color: #e3f2fd; }
            .completed { background-color: #e8f5e8; }
            .failed { background-color: #ffebee; }
        </style>
    </head>
    <body>
        <h1>🐉 D&D SRD Processor</h1>
        <p>Upload your D&D SRD PDF to convert it into RAG-optimized chunks</p>
        
        <div class="upload-area">
            <input type="file" id="pdfFile" accept=".pdf">
            <br><br>
            <button onclick="uploadFile()">Process PDF</button>
        </div>
        
        <div id="status"></div>
        
        <script>
            async function uploadFile() {
                const fileInput = document.getElementById('pdfFile');
                const file = fileInput.files[0];
                if (!file) {
                    alert('Please select a PDF file');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/api/process', {
                        method: 'POST',
                        body: formData
                    });
                    const result = await response.json();
                    
                    if (response.ok) {
                        pollStatus(result.job_id);
                    } else {
                        document.getElementById('status').innerHTML = 
                            `<div class="status failed">Error: ${result.detail}</div>`;
                    }
                } catch (error) {
                    document.getElementById('status').innerHTML = 
                        `<div class="status failed">Error: ${error.message}</div>`;
                }
            }
            
            async function pollStatus(jobId) {
                const statusDiv = document.getElementById('status');
                
                while (true) {
                    try {
                        const response = await fetch(`/api/status/${jobId}`);
                        const status = await response.json();
                        
                        let statusClass = status.status;
                        let statusText = `
                            <div class="status ${statusClass}">
                                <strong>Status:</strong> ${status.status}<br>
                                <strong>Progress:</strong> ${Math.round(status.progress * 100)}%<br>
                                <strong>Current Step:</strong> ${status.current_step}
                        `;
                        
                        if (status.status === 'completed') {
                            statusText += `<br><a href="/api/download/${jobId}">Download Results</a>`;
                            statusDiv.innerHTML = statusText + '</div>';
                            break;
                        } else if (status.status === 'failed') {
                            statusText += `<br><strong>Error:</strong> ${status.error_message}`;
                            statusDiv.innerHTML = statusText + '</div>';
                            break;
                        }
                        
                        statusDiv.innerHTML = statusText + '</div>';
                        await new Promise(resolve => setTimeout(resolve, 2000));
                    } catch (error) {
                        console.error('Error polling status:', error);
                        await new Promise(resolve => setTimeout(resolve, 5000));
                    }
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/process")
async def process_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    config: ProcessingRequest = ProcessingRequest()
):
    """Start PDF processing job."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    file_path = upload_dir / f"{job_id}.pdf"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Create job status
    jobs[job_id] = ProcessingStatus(
        job_id=job_id,
        status="queued",
        progress=0.0,
        current_step="Initializing",
        created_at=datetime.now()
    )
    
    # Start background processing
    background_tasks.add_task(process_pdf_background, job_id, file_path, config)
    
    return {"job_id": job_id, "status": "queued"}

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Get processing status for a job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]

@app.get("/api/download/{job_id}")
async def download_results(job_id: str):
    """Download processed results."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")
    
    # Create zip file with results
    results_dir = Path("results") / job_id
    if not results_dir.exists():
        raise HTTPException(status_code=404, detail="Results not found")
    
    # In a real implementation, create a zip file here
    return {"message": "Download functionality would be implemented here"}

async def process_pdf_background(job_id: str, file_path: Path, config: ProcessingRequest):
    """Background task to process PDF."""
    try:
        job = jobs[job_id]
        
        # Update status: PDF extraction
        job.status = "processing"
        job.current_step = "Extracting text from PDF"
        job.progress = 0.1
        
        # Import and run your existing functions here
        # from srd_processor import extract_text_by_layout, clean_text_to_markdown, etc.
        
        # Simulate processing steps
        await asyncio.sleep(2)  # PDF extraction
        job.current_step = "Basic text cleanup"
        job.progress = 0.3
        
        await asyncio.sleep(3)  # Basic cleanup
        job.current_step = "AI enhancement"
        job.progress = 0.6
        
        await asyncio.sleep(5)  # AI cleanup
        job.current_step = "Creating RAG chunks"
        job.progress = 0.9
        
        await asyncio.sleep(2)  # Chunking
        job.status = "completed"
        job.current_step = "Complete"
        job.progress = 1.0
        job.completed_at = datetime.now()
        
    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        job.completed_at = datetime.now()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
