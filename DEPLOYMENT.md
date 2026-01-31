# Jordan Vectorizer API - PNG to SVG Conversion

## Overview

This API converts **PNG images to high-quality SVG vectors** with configurable parameters for optimal quality and smooth edges.

**Key Features:**
- **Multiple Input Formats:** HTTP/HTTPS URLs, local file paths, or base64 encoded images
- **Always Outputs SVG:** Generates clean, scalable vector graphics
- **Smooth Corners:** Optimized settings for professional quality (cornerThreshold: 75)
- **Static File Serving:** Returns direct URL to download SVG
- **Production Ready:** Fast conversion with optimized defaults

**Input:** PNG image (URL, path, or base64)  
**Output:** SVG file URL + base64 + metadata

---

## How It Works

```
POST /vectorizer/v1/convert
  
Accepts PNG from URL, file path, or base64
  
Returns { url, filename, svg_base64, processingTime, config }
```

**Processing Time:** 8-10 seconds average (varies by image size)  
**Output Location:** `/output` folder with static file serving  
**Security:** No directory traversal, only serves SVG files

---

## Quick Start (Pre-Built Image Available)

A ready-to-use Docker image is available. **You can skip building and go directly to deployment.**

**Docker Image:** `docker.io/igabhix001/jordan-vectorizer:latest`  
**GitHub:** `https://github.com/igabhix001/jordan-vectorizer`

### Important Notes

✅ **Use the pre-built Docker image** - No build tools required  
✅ **Instant deployment** - Pull and deploy to RunPod immediately  
⚠️ **Local development** requires building the Rust native module (see [BUILD_INSTRUCTIONS.md](./BUILD_INSTRUCTIONS.md))

---

## Step 1: Create Runpod Account

1. Go to https://runpod.io
2. Sign up for an account
3. Add credits ($10-20 minimum)

---

## Step 2: Create Serverless Endpoint

1. Go to https://www.runpod.io/console/serverless
2. Click **"New Endpoint"**
3. Click **"Import from Docker Registry"**
4. Enter the image: `docker.io/igabhix001/jordan-vectorizer:latest`
5. Click **"Next"**
6. Configure endpoint:
   - **Name:** Jordan Vectorizer API
   - **Endpoint Type:** Queue
   - **GPU Configuration:** CPU-only (no GPU needed)
   - **Max Workers:** 1-3 (increase for more concurrent requests)
   - **Idle Timeout:** 5 seconds
7. Click **"Deploy Endpoint"**

---

## CPU Selection Guide

**This API runs on CPU** - no GPU required. Select based on your performance needs:

| CPU Type | Generation Time | Cost/hr | Best For |
|----------|-----------------|---------|----------|
| **Standard CPU** | 8-10 seconds | ~$0.10 | Production workloads |
| **High CPU** | 6-8 seconds | ~$0.15 | High-performance |

**Recommendation:** Standard CPU is sufficient for most use cases.

---

## Step 3: Get Your API Credentials

After deployment:
1. Copy your **Endpoint ID** (looks like: `abc123xyz`)
2. Go to **Settings** → **API Keys**
3. Create or copy your **API Key**

---

## Step 4: Test Your API

### Using curl (Linux/Mac)

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "image": "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854619/Charming_Cartoon_Lion_Cub-64933-PNGVerse_przfkt.png"
    }'
```

### Using PowerShell (Windows)

```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_API_KEY"
    "Content-Type" = "application/json"
}
$body = @{
    input = @{
        image = "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854619/Charming_Cartoon_Lion_Cub-64933-PNGVerse_przfkt.png"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" -Method POST -Headers $headers -Body $body
```

---

## Expected Response

```json
{
  "delayTime": 2000,
  "executionTime": 8500,
  "id": "job-id-here",
  "output": {
    "status": "success",
    "url": "http://your-endpoint/files/vector_1234567890_abc123.svg",
    "filename": "vector_1234567890_abc123.svg",
    "svg_base64": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciLi4u",
    "processingTime": 8.523,
    "config": {
      "cornerThreshold": 75,
      "colorPrecision": 8,
      "filterSpeckle": 6,
      "mode": "spline"
    },
    "info": "Generated at 2024-01-31T12:00:00"
  },
  "status": "COMPLETED"
}
```

---

## Step 5: Use Your SVG

The response contains:
- **`url`**: Direct URL to download the SVG file
- **`svg_base64`**: Base64 encoded SVG content to save directly

### Download from URL (PowerShell)
```powershell
$response = Invoke-RestMethod -Uri "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" -Method POST -Headers $headers -Body $body
Invoke-WebRequest -Uri $response.output.url -OutFile "output.svg"
```

### Save from Base64 (Python)
```python
import base64

svg_base64 = response["output"]["svg_base64"]
with open("output.svg", "wb") as f:
    f.write(base64.b64decode(svg_base64))
```

### Save from Base64 (JavaScript/Node.js)
```javascript
const fs = require('fs');
const svgBase64 = response.output.svg_base64;
fs.writeFileSync('output.svg', Buffer.from(svgBase64, 'base64'));
```

---

## API Reference

### Endpoint URL
```
POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync
```

### Headers
| Header | Value |
|--------|-------|
| `Authorization` | `Bearer YOUR_API_KEY` |
| `Content-Type` | `application/json` |

### Request Body (Minimal)
```json
{
  "input": {
    "image": "https://example.com/image.png"
  }
}
```

### Request Body (Full Configuration)
```json
{
  "input": {
    "image": "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854618/Little_Coffee_Buddy-29180-PNGVerse_fefqzb.png",
    "config": {
      "colorMode": "color",
      "colorPrecision": 8,
      "filterSpeckle": 6,
      "spliceThreshold": 45,
      "cornerThreshold": 75,
      "hierarchical": "stacked",
      "mode": "spline",
      "layerDifference": 6,
      "lengthThreshold": 4.0,
      "maxIterations": 3,
      "pathPrecision": 5
    }
  }
}
```

### All Supported Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image` | string | **Yes** | - | PNG image: URL, file path, or base64 |
| `config` | object | No | See below | Vectorization configuration |

### Configuration Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `colorMode` | string | `"color"` | color, binary | Color or black & white |
| `colorPrecision` | int | `8` | 1-8 | Significant bits in RGB channels |
| `filterSpeckle` | int | `6` | ≥0 | Remove patches smaller than X pixels |
| `spliceThreshold` | int | `45` | 0-180 | Minimum angle to splice spline (degrees) |
| `cornerThreshold` | int | `75` | 0-180 | **Minimum angle for smooth corners (degrees)** |
| `hierarchical` | string | `"stacked"` | stacked, cutout | Layer stacking mode |
| `mode` | string | `"spline"` | none, polygon, spline | Path simplification mode |
| `layerDifference` | int | `6` | ≥0 | Color difference between layers |
| `lengthThreshold` | float | `4.0` | ≥0 | Maximum segment length |
| `maxIterations` | int | `3` | ≥1 | Smoothing iterations |
| `pathPrecision` | int | `5` | ≥1 | Decimal places in paths |

---

## Input Formats

The API accepts PNG images in **three formats**:

### 1. HTTP/HTTPS URL
```json
{
  "input": {
    "image": "https://example.com/image.png"
  }
}
```

### 2. Local File Path (for local testing)
```json
{
  "input": {
    "image": "C:\\Users\\abhir\\Downloads\\Testing\\Little_Coffee_Buddy.png"
  }
}
```

### 3. Base64 Encoded String
```json
{
  "input": {
    "image": "iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

Or with data URL prefix:
```json
{
  "input": {
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

---

## Default Configuration

The API uses these optimized defaults for **high quality, smooth output**:

| Parameter | Default Value | Why This Value |
|-----------|---------------|----------------|
| **cornerThreshold** | 75 | Smoother corners and edges |
| **colorPrecision** | 8 | Maximum color accuracy |
| **filterSpeckle** | 6 | Cleaner output, removes noise |
| **mode** | spline | Smoothest curve rendering |
| **maxIterations** | 3 | Better smoothing quality |
| **colorMode** | color | Full color support |
| **hierarchical** | stacked | Better layer handling |

### Important Notes

 **All parameters are optional** except `image`  
 **Any default can be overridden** by specifying it in `config`  
 **Optimized for quality** - settings tuned for smooth, professional output  
 **Processing time** - 8-10 seconds average

---

## Complete Examples

See [TEST_EXAMPLES.md](./TEST_EXAMPLES.md) for full test examples with PowerShell and cURL commands.

---

## Response Format

```json
{
  "status": "COMPLETED",
  "output": {
    "status": "success",
    "url": "http://endpoint/files/vector_timestamp_id.svg",
    "filename": "vector_timestamp_id.svg",
    "svg_base64": "PHN2ZyB4bWxucz0i...",
    "processingTime": 8.523,
    "config": {
      "colorMode": "color",
      "colorPrecision": 8,
      "filterSpeckle": 4,
      "cornerThreshold": 60,
      "mode": "spline",
      "maxIterations": 3
    },
    "info": "Generated at 2024-01-31T12:00:00"
  }
}
```

---

## Pricing

Pricing is based on CPU usage:

| CPU Type | Cost/second | Cost per conversion |
|----------|-------------|---------------------|
| Standard CPU | $0.000028 | ~$0.0002-0.0003 (8-10 sec) |
| High CPU | $0.000042 | ~$0.0003-0.0004 (6-8 sec) |

**Key insight:** Very cost-effective for vector conversion. Choose based on **speed requirements**.

---

## Cold Start Warning

The **first request after idle** takes **30-60 seconds** (cold start) to initialize the Node.js environment.

**Subsequent requests are fast** (8-10 seconds).

### Eliminating Cold Starts

| Strategy | Cold Start | Cost When Idle |
|----------|------------|----------------|
| Min Workers = 0 | 30-60 seconds | $0 |
| Min Workers = 1 | **None** | CPU hourly rate |

**For production:** Set **Min Workers = 1** to keep a worker always warm.

---

## Optimization Tips

### 1. Use Standard CPU
Sufficient for most use cases. No GPU needed.

### 2. Set Min Workers = 1
Eliminates cold start delays. Worker stays warm and ready.

### 3. Use Async Requests for Batches
For multiple images, use `/run` endpoint instead of `/runsync` to queue jobs in parallel.

### 4. Optimize Image Size
Smaller images (under 2048x2048) process faster.

---

## Troubleshooting

### Problem: Request times out
**Solution:** First request has a cold start (30-60 seconds). Wait and check status, or set Min Workers = 1.

### Problem: "Failed to download image from URL"
**Solution:** 
- Verify URL is accessible
- Check if URL requires authentication
- Ensure URL points to a PNG file

### Problem: "Invalid image input"
**Solution:** Check that your input is one of:
- Valid HTTP/HTTPS URL
- Existing local file path
- Valid base64 encoded PNG

### Problem: Status shows "FAILED"
**Solution:** Check error message in response. Common issues:
- Missing `image` field (required)
- Invalid JSON format
- Inaccessible URL
- Invalid base64 encoding

### Problem: Poor quality output
**Solution:**
1. Increase `cornerThreshold` (try 75-80)
2. Increase `filterSpeckle` (try 6-8)
3. Use `mode: "spline"` for smoothest curves
4. Increase `maxIterations` (try 3-4)

---

## Support

If you encounter issues:
1. **Check Runpod logs** for your endpoint (detailed error messages)
2. **Verify API key** is correct and has credits
3. **Validate JSON** format using online JSON validator
4. **Check image format** - must be PNG
5. **Review examples** in TEST_EXAMPLES.md

---

**GitHub:** https://github.com/igabhix001/jordan-vectorizer  
**Docker Image:** docker.io/igabhix001/jordan-vectorizer:latest

*This API is pay-per-use. You are only charged when converting images.*
