# Jordan Vectorizer Test Script
param(
    [string]$InputPath = "C:\Users\abhir\Downloads\Testing\Testing\Little_Coffee_Buddy-29180-PNGVerse.png",
    [string]$OutputPath = "output.svg"
)

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Jordan Vectorizer API Test" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if API is running
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✓ API is healthy" -ForegroundColor Green
}
catch {
    Write-Host "✗ API is not running. Please start it with .\start.bat" -ForegroundColor Red
    exit 1
}

# Check if input file exists
if (-not (Test-Path $InputPath)) {
    Write-Host "✗ Input file not found: $InputPath" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Input file found: $InputPath" -ForegroundColor Green
Write-Host ""

# Convert with high quality settings
Write-Host "Converting PNG to SVG..." -ForegroundColor Yellow

$body = @{
    filePath = $InputPath
    outputPath = $OutputPath
    config = @{
        cornerThreshold = 75
        colorPrecision = 8
        filterSpeckle = 6
        mode = "spline"
        maxIterations = 3
    }
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/convert/path" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host ""
    Write-Host "==================================" -ForegroundColor Green
    Write-Host "✓ Conversion Successful!" -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor Green
    Write-Host "Input:  $($response.inputPath)"
    Write-Host "Output: $($response.outputPath)"
    Write-Host "Time:   $($response.processingTime) seconds"
    Write-Host ""
    Write-Host "Configuration used:" -ForegroundColor Cyan
    $response.config | ConvertTo-Json | Write-Host
}
catch {
    Write-Host ""
    Write-Host "✗ Conversion failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)"
    exit 1
}
