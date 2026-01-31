# @jordan/vectorizer

High-performance PNG to SVG converter built with Rust, featuring a production-ready API for seamless integration. Powered by advanced vectorization algorithms with `O(n)` time complexity.

**GitHub:** https://github.com/igabhix001/jordan-vectorizer  
**Docker Image:** docker.io/igabhix001/jordan-vectorizer:latest

## Quick Start

### Option 1: Use Pre-built Docker Image (Recommended)
```bash
docker pull igabhix001/jordan-vectorizer:latest
docker run -p 8000:8000 igabhix001/jordan-vectorizer:latest
```

### Option 2: Build from Source

**Prerequisites:** Visual Studio Build Tools (Windows), Rust, Node.js 20+

```bash
# Install dependencies
npm install

# Build native module
npm run build

# Start API
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**See [BUILD_INSTRUCTIONS.md](./BUILD_INSTRUCTIONS.md) for detailed build instructions.**

---

If you want to use a synchronous API, you can use `vectorizeSync` instead.

## API

### `vectorize(data: Buffer, config?: Config | Preset): Promise<string>`

Takes an image buffer and returns a promise that resolves to an SVG string.

### `vectorizeSync(data: Buffer, config?: Config | Preset): string`

Takes an image buffer and returns an SVG string synchronously.

### `vectorizeRaw(data: Buffer, args: RawDataConfig, config?: Config | Preset): Promise<string>`

Takes a raw pixel data buffer and returns a promise that resolves to an SVG string.

### `vectorizeRawSync(data: Buffer, args: RawDataConfig, config?: Config | Preset): string`

Takes a raw pixel data buffer and returns an SVG string synchronously.

## Production API

This package includes a production-ready REST API for RunPod serverless deployment.

### Quick Start API

```bash
# Start the API server
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000

# Or use Docker
docker-compose up -d
```

### API Endpoint

**POST** `/vectorizer/v1/convert`

Accepts PNG images from:
- **HTTP/HTTPS URLs** - `"https://example.com/image.png"`
- **Local file paths** - `"C:\\Users\\user\\image.png"` (local testing only)
- **Base64 encoded** - `"iVBORw0KGgoAAAANSUhEUgAA..."`

Returns:
- **Static URL** to download SVG file
- **Base64 encoded** SVG content
- **Processing time** and configuration used

### Example API Usage

**PowerShell (Windows):**
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

# Download the SVG
Invoke-WebRequest -Uri $response.output.url -OutFile "output.svg"
```

**cURL (Linux/Mac):**
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

**For complete API documentation:**
- **Deployment Guide:** [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Test Examples:** [TEST_EXAMPLES.md](./TEST_EXAMPLES.md) (PowerShell & cURL)

## Demo

Generated under the following configuration:

```js
{
    colorMode: ColorMode.Color,
    colorPrecision: 8,
    filterSpeckle: 4,
    spliceThreshold: 45,
    cornerThreshold: 60,
    hierarchical: Hierarchical.Stacked,
    mode: PathSimplifyMode.Spline,
    layerDifference: 6,
    lengthThreshold: 4,
    maxIterations: 2
}
