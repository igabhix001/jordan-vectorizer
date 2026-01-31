# Docker Deployment Guide

## ✅ Docker Image Available

**Docker Hub:** `docker.io/igabhix001/jordan-vectorizer:latest`  
**Image Size:** ~500MB (optimized multi-stage build)  
**Status:** ✅ Built and tested successfully

---

## Quick Test Locally

```powershell
# Pull and run the container
docker pull igabhix001/jordan-vectorizer:latest
docker run -d -p 8000:8000 --name vectorizer igabhix001/jordan-vectorizer:latest

# Wait 5 seconds for startup
Start-Sleep -Seconds 5

# Test health endpoint
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Test conversion with URL
$response = Invoke-RestMethod -Uri "http://localhost:8000/vectorizer/v1/convert" -Method POST -ContentType "application/json" -Body (@{ image = "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854619/Charming_Cartoon_Lion_Cub-64933-PNGVerse_przfkt.png" } | ConvertTo-Json)

# Stop and remove container
docker stop vectorizer
docker rm vectorizer
```

---

## Deploy to RunPod Serverless

### Step 1: Create RunPod Account
1. Go to https://runpod.io
2. Sign up and add credits ($10-20 minimum)

### Step 2: Create Serverless Endpoint
1. Navigate to **Serverless** → **+ New Endpoint**
2. Configure:
   - **Name:** `jordan-vectorizer`
   - **Docker Image:** `igabhix001/jordan-vectorizer:latest`
   - **Container Disk:** 10 GB
   - **GPU Type:** CPU (no GPU needed)
   - **Active Workers:** 0 (auto-scale)
   - **Max Workers:** 3
   - **Idle Timeout:** 5 seconds
   - **Execution Timeout:** 120 seconds

### Step 3: Get API Key
1. Go to **Settings** → **API Keys**
2. Create new API key
3. Copy the key (starts with `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### Step 4: Get Endpoint ID
1. Go to your endpoint
2. Copy the **Endpoint ID** from the URL or dashboard

---

## Test RunPod Deployment

### PowerShell
```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_API_KEY"
    "Content-Type" = "application/json"
}

$body = @{
    input = @{
        image = "https://example.com/image.png"
        config = @{
            cornerThreshold = 75
            colorPrecision = 8
            filterSpeckle = 6
        }
    }
} | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod -Uri "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" -Method POST -Headers $headers -Body $body

Write-Host "Status: $($response.status)"
Write-Host "SVG URL: $($response.output.url)"
Write-Host "Processing time: $($response.output.processingTime) seconds"
```

### cURL
```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "image": "https://example.com/image.png",
      "config": {
        "cornerThreshold": 75,
        "colorPrecision": 8,
        "filterSpeckle": 6
      }'
```

---

## Input Formats Supported

### 1. HTTP/HTTPS URL
```json
{
  "input": {
    "image": "https://example.com/image.png"
  }
}
```

### 2. Base64 Encoded
```json
{
  "input": {
    "image": "iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

### 3. Base64 with Data URL Prefix
```json
{
  "input": {
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

---

## Response Format

```json
{
  "status": "COMPLETED",
  "output": {
    "url": "http://your-endpoint/files/vector_1234567890_abc123.svg",
    "filename": "vector_1234567890_abc123.svg",
    "svg_base64": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPi4uLjwvc3ZnPg==",
    "processingTime": 3.854,
    "config": {
      "colorMode": "color",
      "colorPrecision": 8,
      "filterSpeckle": 6,
      "cornerThreshold": 75,
      ...
    }
  }
}
```

---

## Configuration Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `colorMode` | string | `"color"` | `"color"` or `"binary"` | Color or black & white |
| `colorPrecision` | int | `8` | 1-8 | Significant bits in RGB |
| `filterSpeckle` | int | `6` | 0+ | Discard patches smaller than X pixels |
| `cornerThreshold` | int | `75` | 0-180 | Minimum angle for corners (degrees) |
| `spliceThreshold` | int | `45` | 0-180 | Minimum angle to splice spline (degrees) |
| `layerDifference` | int | `6` | 0+ | Color difference between layers |
| `lengthThreshold` | float | `4.0` | 0+ | Maximum segment length |
| `maxIterations` | int | `3` | 1+ | Maximum smoothing iterations |
| `pathPrecision` | int | `5` | 1+ | Decimal places in path |
| `hierarchical` | string | `"stacked"` | `"stacked"` or `"cutout"` | Layer mode |
| `mode` | string | `"spline"` | `"none"`, `"polygon"`, `"spline"` | Path simplification |

---

## Pricing Estimate

**RunPod CPU Pricing:** ~$0.0002/second  
**Average Processing Time:** 3-5 seconds per image  
**Cost per conversion:** ~$0.001 (0.1 cents)

**Example:** 1000 conversions = ~$1.00

---

## Troubleshooting

### Container Not Starting
- Check Docker image name is correct: `igabhix001/jordan-vectorizer:latest`
- Ensure port 8000 is exposed
- Check container logs: `docker logs vectorizer`

### Slow Cold Starts
- RunPod serverless has cold start time (~10-15 seconds)
- Keep workers active by setting min workers > 0
- Or accept cold start delay for cost savings

### Image Download Fails
- Ensure image URL is publicly accessible
- Check image format is PNG
- Try base64 encoding for private images

---

## GitHub Repository

**Source Code:** https://github.com/igabhix001/jordan-vectorizer  
**Issues:** https://github.com/igabhix001/jordan-vectorizer/issues

---

## Support

For issues or questions:
1. Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed API documentation
2. Check [TEST_EXAMPLES.md](./TEST_EXAMPLES.md) for more examples
3. Open an issue on GitHub
