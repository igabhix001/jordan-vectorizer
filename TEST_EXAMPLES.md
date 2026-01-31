# Complete API Test Examples

## Test 1: Simple Conversion from URL 🌐

### Full Payload
```json
{
  "input": {
    "image": "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854619/Charming_Cartoon_Lion_Cub-64933-PNGVerse_przfkt.png"
  }
}
```

### PowerShell Command
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

$response = Invoke-RestMethod -Uri "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" -Method POST -Headers $headers -Body $body

# Download the SVG
Invoke-WebRequest -Uri $response.output.url -OutFile "output.svg"
Write-Host "Saved to: output.svg"
Write-Host "Processing time: $($response.output.processingTime) seconds"
```

### Curl Command
```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "image": "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854619/Charming_Cartoon_Lion_Cub-64933-PNGVerse_przfkt.png"
    }
  }'
```

---

## Test 2: High Quality Conversion with Custom Config 🎨

### Full Payload
```json
{
  "input": {
    "image": "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854618/Little_Coffee_Buddy-29180-PNGVerse_fefqzb.png",
    "config": {
      "cornerThreshold": 60,
      "colorPrecision": 8,
      "filterSpeckle": 4,
      "spliceThreshold": 45,
      "layerDifference": 6,
      "lengthThreshold": 4.0,
      "maxIterations": 2
    }
  }
}
```

### PowerShell Command
```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_API_KEY"
    "Content-Type" = "application/json"
}
$body = @{
    input = @{
        image = "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854618/Little_Coffee_Buddy-29180-PNGVerse_fefqzb.png"
        config = @{
            cornerThreshold = 60
            colorPrecision = 8
            filterSpeckle = 4
            spliceThreshold = 45
            layerDifference = 6
            lengthThreshold = 4.0
            maxIterations = 2
        }
    }
} | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod -Uri "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" -Method POST -Headers $headers -Body $body

# Save from base64
$svgBytes = [System.Convert]::FromBase64String($response.output.svg_base64)
[System.IO.File]::WriteAllBytes("output_high_quality.svg", $svgBytes)

Write-Host "✓ Conversion successful!"
Write-Host "Processing time: $($response.output.processingTime) seconds"
Write-Host "Config used: $($response.output.config | ConvertTo-Json)"
```

### Curl Command
```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "image": "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854618/Little_Coffee_Buddy-29180-PNGVerse_fefqzb.png",
      "config": {
        "cornerThreshold": 60,
        "colorPrecision": 8,
        "filterSpeckle": 4,
        "spliceThreshold": 45,
        "layerDifference": 6,
        "lengthThreshold": 4.0,
        "maxIterations": 2
      }
    }
  }'
```

---

## Test 3: Local File Path (For Local Testing) 📁

The API supports **two request formats**:

### Format 1: Direct (Simpler for local testing)
```json
{
  "image": "D:\\vectorizer-main\\vectorizer-main\\testing_images\\Little_Coffee_Buddy-29180-PNGVerse.png",
  "config": {
    "cornerThreshold": 75,
    "colorPrecision": 8,
    "filterSpeckle": 6
  }
}
```

### Format 2: RunPod Wrapper (For RunPod deployment)
```json
{
  "input": {
    "image": "D:\\vectorizer-main\\vectorizer-main\\testing_images\\Little_Coffee_Buddy-29180-PNGVerse.png",
    "config": {
      "cornerThreshold": 75,
      "colorPrecision": 8,
      "filterSpeckle": 6
    }
  }
}
```

### PowerShell Command (Direct Format - Recommended for Local)
```powershell
$body = @{
    image = "D:\vectorizer-main\vectorizer-main\testing_images\Little_Coffee_Buddy-29180-PNGVerse.png"
    config = @{
        cornerThreshold = 75
        colorPrecision = 8
        filterSpeckle = 6
    }
} | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod -Uri "http://localhost:8000/vectorizer/v1/convert" -Method POST -Body $body -ContentType "application/json"

Write-Host "✓ Saved to: $($response.filename)"
Write-Host "URL: $($response.url)"
Write-Host "Processing time: $($response.processingTime) seconds"
```

### PowerShell Command (RunPod Format)
```powershell
$body = @{
    input = @{
        image = "D:\vectorizer-main\vectorizer-main\testing_images\Little_Coffee_Buddy-29180-PNGVerse.png"
        config = @{
            cornerThreshold = 75
            colorPrecision = 8
            filterSpeckle = 6
        }
    }
} | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod -Uri "http://localhost:8000/vectorizer/v1/convert" -Method POST -Body $body -ContentType "application/json"

Write-Host "✓ Saved to: $($response.filename)"
Write-Host "URL: $($response.url)"
Write-Host "Processing time: $($response.processingTime) seconds"
```

**Note:** Local file paths only work when testing locally. For RunPod deployment, use URLs or base64.

---

## Test 4: Base64 Encoded Image 📦

### Full Payload
```json
{
  "input": {
    "image": "iVBORw0KGgoAAAANSUhEUgAA...(base64 encoded PNG)",
    "config": {
      "cornerThreshold": 75,
      "colorPrecision": 8
    }
  }
}
```

### PowerShell Command
```powershell
# Read and encode image
$imageBytes = [System.IO.File]::ReadAllBytes("C:\path\to\image.png")
$imageBase64 = [System.Convert]::ToBase64String($imageBytes)

$headers = @{
    "Authorization" = "Bearer YOUR_API_KEY"
    "Content-Type" = "application/json"
}
$body = @{
    input = @{
        image = $imageBase64
        config = @{
            cornerThreshold = 75
            colorPrecision = 8
        }
    }
} | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod -Uri "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" -Method POST -Headers $headers -Body $body

# Save the SVG
$svgBytes = [System.Convert]::FromBase64String($response.output.svg_base64)
[System.IO.File]::WriteAllBytes("output.svg", $svgBytes)

Write-Host "✓ Conversion complete!"
```

---

## Test 5: Batch Conversion (Multiple Images) 🔄

### PowerShell Script
```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_API_KEY"
    "Content-Type" = "application/json"
}

$imageUrls = @(
    "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854619/Charming_Cartoon_Lion_Cub-64933-PNGVerse_przfkt.png",
    "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854618/Little_Coffee_Buddy-29180-PNGVerse_fefqzb.png",
    "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854617/Gamer_Kid_in_Action-32251-PNGVerse_wzicpr.png"
)

$config = @{
    cornerThreshold = 60
    colorPrecision = 8
    filterSpeckle = 4
    maxIterations = 2
}

foreach ($url in $imageUrls) {
    Write-Host "Converting: $url"
    
    $body = @{
        input = @{
            image = $url
            config = $config
        }
    } | ConvertTo-Json -Depth 3
    
    try {
        $response = Invoke-RestMethod -Uri "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" -Method POST -Headers $headers -Body $body
        
        $filename = $response.output.filename
        Invoke-WebRequest -Uri $response.output.url -OutFile $filename
        
        Write-Host "✓ Saved: $filename" -ForegroundColor Green
        Write-Host "  Time: $($response.output.processingTime) seconds`n"
    }
    catch {
        Write-Host "✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "Batch conversion complete!"
```

---

## Test 6: Binary Mode (Black & White) ⚫⚪

### Full Payload
```json
{
  "input": {
    "image": "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854617/Gamer_Kid_in_Action-32251-PNGVerse_wzicpr.png",
    "config": {
      "colorMode": "binary",
      "filterSpeckle": 4,
      "cornerThreshold": 90
    }
  }
}
```

### PowerShell Command
```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_API_KEY"
    "Content-Type" = "application/json"
}
$body = @{
    input = @{
        image = "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854617/Gamer_Kid_in_Action-32251-PNGVerse_wzicpr.png"
        config = @{
            colorMode = "binary"
            filterSpeckle = 4
            cornerThreshold = 90
        }
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" -Method POST -Headers $headers -Body $body
```

---

## Test 7: Maximum Quality Settings 🌟

### Full Payload
```json
{
  "input": {
    "image": "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854619/Charming_Cartoon_Lion_Cub-64933-PNGVerse_przfkt.png",
    "config": {
      "colorMode": "color",
      "colorPrecision": 8,
      "filterSpeckle": 4,
      "cornerThreshold": 60,
      "spliceThreshold": 45,
      "layerDifference": 6,
      "lengthThreshold": 4.0,
      "maxIterations": 2,
      "pathPrecision": 5
    }
  }
}
```

### PowerShell Command
```powershell
$headers = @{
    "Authorization" = "Bearer YOUR_API_KEY"
    "Content-Type" = "application/json"
}
$body = @{
    input = @{
        image = "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854619/Charming_Cartoon_Lion_Cub-64933-PNGVerse_przfkt.png"
        config = @{
            colorMode = "color"
            colorPrecision = 8
            filterSpeckle = 4
            cornerThreshold = 60
            spliceThreshold = 45
            layerDifference = 6
            lengthThreshold = 4.0
            maxIterations = 2
            pathPrecision = 5
        }
    }
} | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod -Uri "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" -Method POST -Headers $headers -Body $body

Write-Host "Maximum quality conversion complete!"
Write-Host "Processing time: $($response.output.processingTime) seconds"
```

---

## Test 8: Python Script 🐍

```python
import requests
import json
import base64

# API configuration
ENDPOINT_ID = "YOUR_ENDPOINT_ID"
API_KEY = "YOUR_API_KEY"
API_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"

# Test with URL
payload = {
    "input": {
        "image": "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854618/Little_Coffee_Buddy-29180-PNGVerse_fefqzb.png",
        "config": {
            "cornerThreshold": 60,
            "colorPrecision": 8,
            "filterSpeckle": 4,
            "maxIterations": 2
        }
    }
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Make request
response = requests.post(API_URL, json=payload, headers=headers)
result = response.json()

# Save the SVG
if result["status"] == "COMPLETED":
    svg_base64 = result["output"]["svg_base64"]
    with open("output.svg", "wb") as f:
        f.write(base64.b64decode(svg_base64))
    print(f"✓ SVG saved: {result['output']['filename']}")
    print(f"Processing time: {result['output']['processingTime']} seconds")
else:
    print(f"✗ Error: {result}")
```

---

## Test 9: Node.js/JavaScript Script 📜

```javascript
const axios = require('axios');
const fs = require('fs');

const ENDPOINT_ID = 'YOUR_ENDPOINT_ID';
const API_KEY = 'YOUR_API_KEY';
const API_URL = `https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync`;

const payload = {
  input: {
    image: 'https://res.cloudinary.com/dbur7qch9/image/upload/v1769854618/Little_Coffee_Buddy-29180-PNGVerse_fefqzb.png',
    config: {
      cornerThreshold: 60,
      colorPrecision: 8,
      filterSpeckle: 4,
      maxIterations: 2
    }
  }
};

const headers = {
  'Authorization': `Bearer ${API_KEY}`,
  'Content-Type': 'application/json'
};

axios.post(API_URL, payload, { headers })
  .then(response => {
    const result = response.data;
    if (result.status === 'COMPLETED') {
      const svgBase64 = result.output.svg_base64;
      fs.writeFileSync('output.svg', Buffer.from(svgBase64, 'base64'));
      console.log(`✓ SVG saved: ${result.output.filename}`);
      console.log(`Processing time: ${result.output.processingTime} seconds`);
    }
  })
  .catch(error => console.error('✗ Error:', error.message));
```

---

## All Available Configuration Parameters

### Complete Parameter List
```json
{
  "input": {
    // REQUIRED
    "image": "URL, file path, or base64 string",
    
    // OPTIONAL CONFIGURATION
    "config": {
      // QUALITY SETTINGS
      "colorMode": "color",
      "colorPrecision": 8,
      "filterSpeckle": 6,
      "cornerThreshold": 75,
      "mode": "spline",
      "maxIterations": 3,
      
      // ADVANCED SETTINGS
      "spliceThreshold": 45,
      "hierarchical": "stacked",
      "layerDifference": 6,
      "lengthThreshold": 4.0,
      "pathPrecision": 5
    }
  }
}
```

---

## Configuration Presets

### Default (Balanced Quality)
```json
{
  "config": {
    "cornerThreshold": 75,
    "colorPrecision": 8,
    "filterSpeckle": 6,
    "mode": "spline",
    "maxIterations": 3
  }
}
```

### High Quality (Smooth & Clean)
```json
{
  "config": {
    "cornerThreshold": 80,
    "colorPrecision": 8,
    "filterSpeckle": 8,
    "mode": "spline",
    "maxIterations": 4,
    "lengthThreshold": 3.0
  }
}
```

### Fast (Lower Quality)
```json
{
  "config": {
    "cornerThreshold": 60,
    "colorPrecision": 6,
    "filterSpeckle": 4,
    "mode": "polygon",
    "maxIterations": 2
  }
}
```

### Logo/Icon Optimized
```json
{
  "config": {
    "cornerThreshold": 80,
    "colorPrecision": 8,
    "filterSpeckle": 8,
    "mode": "spline",
    "maxIterations": 4
  }
}
```

---

## Response Format

```json
{
  "delayTime": 2000,
  "executionTime": 8500,
  "id": "job-abc123",
  "output": {
    "status": "success",
    "url": "http://endpoint/files/vector_1234567890_abc123.svg",
    "filename": "vector_1234567890_abc123.svg",
    "svg_base64": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDI0IiBoZWlnaHQ9IjEwMjQiPi4uLjwvc3ZnPg==",
    "processingTime": 8.523,
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
    },
    "info": "Generated at 2024-01-31T12:00:00"
  },
  "status": "COMPLETED"
}
```

- `url`: Direct URL to download the SVG file (accessible via HTTP)
- `filename`: Filename of the generated SVG
- `svg_base64`: Base64 encoded SVG content (can be decoded and saved directly)
- `processingTime`: Time taken to convert in seconds
- `config`: Configuration used for conversion
- `info`: Generation timestamp

---

## Input Format Summary

| Format | Example | Use Case |
|--------|---------|----------|
| **HTTP/HTTPS URL** | `"https://example.com/image.png"` | Remote images, production |
| **Local File Path** | `"C:\\Users\\user\\image.png"` | Local testing only |
| **Base64 String** | `"iVBORw0KGgoAAAANSUhEUgAA..."` | Embedded images, API integration |
| **Data URL** | `"data:image/png;base64,iVBORw0..."` | Browser uploads |

---

## Tips for Best Results

1. **For smooth corners:** Set `cornerThreshold` to 75-80
2. **For clean output:** Set `filterSpeckle` to 6-8
3. **For best quality:** Use `mode: "spline"` with `maxIterations: 3-4`
4. **For logos:** Increase `cornerThreshold` and `filterSpeckle`
5. **For photos:** Use default settings with `colorPrecision: 8`

---

**GitHub:** https://github.com/igabhix001/jordan-vectorizer  
**Docker Image:** docker.io/igabhix001/jordan-vectorizer:latest
