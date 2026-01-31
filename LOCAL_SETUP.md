# Local Development Setup

## ⚠️ Important: Build Required

The local API server requires the **Rust native module** to be built before it can run. This is a one-time setup.

---

## Quick Setup (Windows)

```powershell
# Step 1: Install Visual Studio Build Tools (if not already installed)
winget install Microsoft.VisualStudio.2022.BuildTools

# Step 2: Install Rust (if not already installed)
winget install Rustlang.Rustup

# Step 3: Restart PowerShell to refresh PATH

# Step 4: Build the native module
cd d:\vectorizer-main\vectorizer-main
npm install
npm run build

# Step 5: Start the API server
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Verify Build Success

After running `npm run build`, you should see a `.node` file:

```powershell
# Check if the native module was built
ls *.node

# Expected output:
# vectorizer.win32-x64-msvc.node
```

---

## Test the Local Server

### Test with URL (requires internet)
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:8000/vectorizer/v1/convert" -Method POST -ContentType "application/json" -Body (@{
    image = "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854619/Charming_Cartoon_Lion_Cub-64933-PNGVerse_przfkt.png"
    config = @{
        cornerThreshold = 60
        colorPrecision = 8
        filterSpeckle = 4
    }
} | ConvertTo-Json -Depth 3)

Write-Host "✓ SVG Generated: $($response.filename)" -ForegroundColor Green
Write-Host "URL: $($response.url)" -ForegroundColor Cyan
Write-Host "Processing time: $($response.processingTime) seconds" -ForegroundColor Yellow
```

### Test with Local File
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:8000/vectorizer/v1/convert" -Method POST -ContentType "application/json" -Body (@{
    image = "D:\vectorizer-main\vectorizer-main\testing_images\Little_Coffee_Buddy-29180-PNGVerse.png"
    config = @{
        cornerThreshold = 60
        colorPrecision = 8
        filterSpeckle = 4
    }
} | ConvertTo-Json -Depth 3)

Write-Host "✓ SVG Generated: $($response.filename)" -ForegroundColor Green
Write-Host "URL: $($response.url)" -ForegroundColor Cyan
```

---

## Troubleshooting

### Error: "Cannot find module '@neplex/vectorizer-win32-x64-msvc'"

**Cause:** The native Rust module hasn't been built yet.

**Solution:**
```powershell
npm run build
```

### Error: "linker `link.exe` not found"

**Cause:** Visual Studio Build Tools not installed or not in PATH.

**Solution:**
```powershell
# Install Visual Studio Build Tools
winget install Microsoft.VisualStudio.2022.BuildTools

# Restart PowerShell
```

### Error: "Command timed out after 120 seconds"

**Cause:** The CLI is trying to load the native module but it doesn't exist.

**Solution:**
```powershell
# Build the native module first
npm run build

# Then restart the API server
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Alternative: Use Docker (No Build Required)

If you don't want to build locally, use the Docker image:

```powershell
docker pull igabhix001/jordan-vectorizer:latest
docker run -d -p 8000:8000 igabhix001/jordan-vectorizer:latest

# Test it
$response = Invoke-RestMethod -Uri "http://localhost:8000/vectorizer/v1/convert" -Method POST -ContentType "application/json" -Body (@{
    image = "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854619/Charming_Cartoon_Lion_Cub-64933-PNGVerse_przfkt.png"
} | ConvertTo-Json)
```

---

## Default Configuration

The API uses these default parameters (optimized for quality):

```json
{
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
```

You can override any parameter in your request.

---

## Development Workflow

```powershell
# 1. Make changes to the code
# 2. If you changed Rust code, rebuild:
npm run build

# 3. If you changed Python code, the server will auto-reload
# (if started with --reload flag)

# 4. Test your changes
$response = Invoke-RestMethod -Uri "http://localhost:8000/vectorizer/v1/convert" -Method POST -ContentType "application/json" -Body (@{
    image = "https://res.cloudinary.com/dbur7qch9/image/upload/v1769854618/Little_Coffee_Buddy-29180-PNGVerse_fefqzb.png"
} | ConvertTo-Json)
```
