# Test script for Jordan Vectorizer API
# Tests both direct and RunPod request formats

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Jordan Vectorizer API Test" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Direct format (for local testing)
Write-Host "Test 1: Direct format" -ForegroundColor Yellow
$body1 = @{
    image = "D:\vectorizer-main\vectorizer-main\testing_images\Little_Coffee_Buddy-29180-PNGVerse.png"
    config = @{
        cornerThreshold = 75
        colorPrecision = 8
        filterSpeckle = 6
    }
} | ConvertTo-Json -Depth 3

try {
    $response1 = Invoke-RestMethod -Uri "http://localhost:8000/vectorizer/v1/convert" -Method POST -Body $body1 -ContentType "application/json"
    Write-Host "✓ Direct format works!" -ForegroundColor Green
    Write-Host "  Filename: $($response1.filename)" -ForegroundColor Gray
    Write-Host "  URL: $($response1.url)" -ForegroundColor Gray
    Write-Host "  Processing time: $($response1.processingTime) seconds" -ForegroundColor Gray
    Write-Host ""
}
catch {
    Write-Host "✗ Direct format failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 2: RunPod format (with input wrapper)
Write-Host "Test 2: RunPod format (with input wrapper)" -ForegroundColor Yellow
$body2 = @{
    input = @{
        image = "D:\vectorizer-main\vectorizer-main\testing_images\Little_Coffee_Buddy-29180-PNGVerse.png"
        config = @{
            cornerThreshold = 75
            colorPrecision = 8
            filterSpeckle = 6
        }
    }
} | ConvertTo-Json -Depth 3

try {
    $response2 = Invoke-RestMethod -Uri "http://localhost:8000/vectorizer/v1/convert" -Method POST -Body $body2 -ContentType "application/json"
    Write-Host "✓ RunPod format works!" -ForegroundColor Green
    Write-Host "  Filename: $($response2.filename)" -ForegroundColor Gray
    Write-Host "  URL: $($response2.url)" -ForegroundColor Gray
    Write-Host "  Processing time: $($response2.processingTime) seconds" -ForegroundColor Gray
    Write-Host ""
}
catch {
    Write-Host "✗ RunPod format failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Tests Complete!" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
