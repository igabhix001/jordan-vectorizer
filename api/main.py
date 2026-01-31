"""
Jordan Vectorizer API - PNG to SVG Conversion
Accepts: HTTP/HTTPS URLs, local file paths, or base64 encoded images
Returns: Static URL to generated SVG file
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional
import subprocess
import tempfile
import os
import uuid
import time
import requests
import base64
import json
from pathlib import Path
from datetime import datetime

app = FastAPI(
    title="Jordan Vectorizer API",
    description="High-performance PNG to SVG conversion API",
    version="1.0.0"
)

# Create output directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Mount static files for serving SVG outputs
app.mount("/files", StaticFiles(directory=str(OUTPUT_DIR), html=False), name="files")

class VectorizerConfig(BaseModel):
    """Configuration for vectorization process"""
    colorMode: Optional[str] = Field(default="color", description="Color mode: 'color' or 'binary'")
    colorPrecision: Optional[int] = Field(default=8, ge=1, le=8, description="Number of significant bits in RGB (1-8)")
    filterSpeckle: Optional[int] = Field(default=4, ge=0, description="Discard patches smaller than X pixels")
    spliceThreshold: Optional[int] = Field(default=45, ge=0, le=180, description="Minimum angle to splice spline (degrees)")
    cornerThreshold: Optional[int] = Field(default=75, ge=0, le=180, description="Minimum angle for corners (degrees)")
    hierarchical: Optional[str] = Field(default="stacked", description="Hierarchical mode: 'stacked' or 'cutout'")
    mode: Optional[str] = Field(default="spline", description="Path simplify mode: 'none', 'polygon', or 'spline'")
    layerDifference: Optional[int] = Field(default=6, ge=0, description="Color difference between gradient layers")
    lengthThreshold: Optional[float] = Field(default=4.0, ge=0, description="Maximum segment length for smoothing")
    maxIterations: Optional[int] = Field(default=3, ge=1, description="Maximum smoothing iterations")
    pathPrecision: Optional[int] = Field(default=5, ge=1, description="Decimal places in path string")

class ConversionRequest(BaseModel):
    """Request model for PNG to SVG conversion"""
    image: str = Field(..., description="PNG image as: HTTP/HTTPS URL, local file path, or base64 string")
    config: Optional[VectorizerConfig] = Field(default=None, description="Optional vectorizer configuration")

class RunPodRequest(BaseModel):
    """RunPod wrapper format"""
    input: ConversionRequest = Field(..., description="Input data for conversion")

def get_default_config() -> dict:
    """Returns default configuration optimized for quality"""
    return {
        "colorMode": "color",
        "colorPrecision": 8,
        "filterSpeckle": 4,
        "spliceThreshold": 45,
        "cornerThreshold": 60,
        "hierarchical": "stacked",
        "mode": "spline",
        "layerDifference": 6,
        "lengthThreshold": 4.0,
        "maxIterations": 2,
        "pathPrecision": 5
    }

def merge_config(user_config: Optional[VectorizerConfig]) -> dict:
    """Merge user config with defaults"""
    default = get_default_config()
    
    if user_config is None:
        return default
    
    user_dict = user_config.dict(exclude_none=True)
    default.update(user_dict)
    return default

def download_image_from_url(url: str) -> bytes:
    """Download image from HTTP/HTTPS URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to download image from URL: {str(e)}")

def load_image_data(image_input: str) -> bytes:
    """
    Load image data from:
    1. HTTP/HTTPS URL
    2. Local file path
    3. Base64 encoded string
    """
    # Check if it's a URL
    if image_input.startswith(('http://', 'https://')):
        return download_image_from_url(image_input)
    
    # Check if it's a local file path
    if os.path.exists(image_input):
        try:
            with open(image_input, 'rb') as f:
                return f.read()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read local file: {str(e)}")
    
    # Try to decode as base64
    try:
        # Remove data URL prefix if present
        if image_input.startswith('data:image'):
            image_input = image_input.split(',', 1)[1]
        return base64.b64decode(image_input)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid image input. Must be: HTTP/HTTPS URL, local file path, or base64 string"
        )

def convert_png_to_svg(png_data: bytes, config: dict, output_filename: str) -> tuple:
    """
    Convert PNG to SVG using the Node.js vectorizer
    Returns: (svg_content, processing_time)
    """
    start_time = time.time()
    
    # Create temp PNG file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as png_file:
        png_file.write(png_data)
        png_path = png_file.name
    
    # Output path in output folder
    output_path = OUTPUT_DIR / output_filename
    
    try:
        # Prepare config as JSON string
        config_json = json.dumps(config)
        
        # Get path to wrapper script
        wrapper_path = Path(__file__).parent / 'vectorizer_wrapper.js'
        
        # Run Node.js wrapper
        cmd = ['node', str(wrapper_path), png_path, str(output_path), config_json]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            raise Exception(f"Vectorizer failed: {result.stderr}")
        
        # Read the generated SVG
        with open(output_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        processing_time = time.time() - start_time
        
        return svg_content, processing_time
        
    finally:
        # Clean up temp PNG file
        if os.path.exists(png_path):
            os.unlink(png_path)

@app.get("/")
async def root():
    """API information"""
    return {
        "status": "healthy",
        "service": "Jordan Vectorizer API",
        "version": "1.0.0",
        "github": "https://github.com/igabhix001/jordan-vectorizer",
        "endpoints": {
            "convert": "POST /vectorizer/v1/convert",
            "health": "GET /health",
            "config": "GET /config/default"
        },
        "input_formats": [
            "HTTP/HTTPS URL",
            "Local file path",
            "Base64 encoded string"
        ]
    }

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}

@app.get("/config/default")
async def get_default_config_endpoint():
    """Get default configuration"""
    return {
        "config": get_default_config(),
        "description": "Default configuration optimized for high quality output"
    }

@app.post("/vectorizer/v1/convert")
async def convert(body: dict):
    """
    Convert PNG to SVG
    
    Accepts both formats:
    1. Direct: {"image": "...", "config": {...}}
    2. RunPod: {"input": {"image": "...", "config": {...}}}
    
    Input formats:
    - HTTP/HTTPS URL: "https://example.com/image.png"
    - Local file path: "C:\\Users\\user\\image.png" or "/path/to/image.png"
    - Base64: "iVBORw0KGgoAAAANSUhEUgAA..." or "data:image/png;base64,iVBORw0..."
    
    Returns:
    - url: Static URL to download the SVG file
    - filename: Name of the generated SVG file
    - svg_base64: Base64 encoded SVG content
    - processingTime: Time taken to convert
    - config: Configuration used
    """
    try:
        # Handle both direct and RunPod wrapped format
        if "input" in body:
            # RunPod format: {"input": {"image": "...", "config": {...}}}
            request_data = body["input"]
        else:
            # Direct format: {"image": "...", "config": {...}}
            request_data = body
        
        # Validate and parse request
        request = ConversionRequest(**request_data)
        
        # Load PNG data
        png_data = load_image_data(request.image)
        
        # Merge configuration
        config = merge_config(request.config)
        
        # Generate unique filename
        timestamp = int(time.time())
        unique_id = uuid.uuid4().hex[:8]
        filename = f"vector_{timestamp}_{unique_id}.svg"
        
        # Convert PNG to SVG
        svg_content, processing_time = convert_png_to_svg(png_data, config, filename)
        
        # Get base URL from request
        base_url = "http://localhost:8000"  # Will be overridden by actual host
        file_url = f"{base_url}/files/{filename}"
        
        # Encode SVG to base64
        svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
        
        return {
            "status": "success",
            "url": file_url,
            "filename": filename,
            "svg_base64": svg_base64,
            "processingTime": processing_time,
            "config": config,
            "info": f"Generated at {datetime.now().isoformat()}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

@app.get("/files/{filename}")
async def get_file(filename: str):
    """
    Serve generated SVG files
    Security: Only serves files from output directory, no directory traversal
    """
    file_path = OUTPUT_DIR / filename
    
    # Security check: ensure file is in output directory
    try:
        file_path = file_path.resolve()
        OUTPUT_DIR.resolve()
        if not str(file_path).startswith(str(OUTPUT_DIR.resolve())):
            raise HTTPException(status_code=403, detail="Access denied")
    except:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        media_type="image/svg+xml",
        filename=filename
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
