# check_ollama.ps1 - Complete Ollama health check (FIXED)
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "🔍 OLLAMA HEALTH CHECK" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan

$ollamaPath = "C:\Users\Thanu\AppData\Local\Programs\Ollama\ollama.exe"

# Test 1: Check if file exists
Write-Host "`n1. Checking if Ollama is installed..." -ForegroundColor Yellow
if (Test-Path $ollamaPath) {
    Write-Host "   ✅ Ollama found at: $ollamaPath" -ForegroundColor Green
} else {
    Write-Host "   ❌ Ollama NOT found at: $ollamaPath" -ForegroundColor Red
    exit
}

# Test 2: Check version
Write-Host "`n2. Checking Ollama version..." -ForegroundColor Yellow
try {
    $version = & $ollamaPath --version
    Write-Host "   ✅ $version" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Failed to get version" -ForegroundColor Red
}

# Test 3: Check if service is running
Write-Host "`n3. Checking if Ollama service is running..." -ForegroundColor Yellow
$process = Get-Process ollama -ErrorAction SilentlyContinue
if ($process) {
    Write-Host "   ✅ Ollama is running (PID: $($process.Id))" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ Ollama service is NOT running" -ForegroundColor Yellow
}

# Test 4: Check available models
Write-Host "`n4. Checking available models..." -ForegroundColor Yellow
try {
    $models = & $ollamaPath list
    Write-Host "   ✅ Models found:" -ForegroundColor Green
    Write-Host $models
} catch {
    Write-Host "   ❌ Failed to list models" -ForegroundColor Red
}

# Test 5: Check if llama3.2:1b is available
Write-Host "`n5. Checking required model (llama3.2:1b)..." -ForegroundColor Yellow
$modelList = & $ollamaPath list
if ($modelList -like "*llama3.2:1b*") {
    Write-Host "   ✅ llama3.2:1b model is available" -ForegroundColor Green
} else {
    Write-Host "   ⚠️ llama3.2:1b model NOT found" -ForegroundColor Yellow
    Write-Host "   Download with: & `"$ollamaPath`" pull llama3.2:1b" -ForegroundColor Yellow
}

# Test 6: Test AI response
Write-Host "`n6. Testing AI response (may take 5-10 seconds)..." -ForegroundColor Yellow
try {
    $response = & $ollamaPath run llama3.2:1b "Say hello" 2>$null
    if ($response) {
        $shortResponse = $response.Substring(0, [Math]::Min(100, $response.Length))
        Write-Host "   ✅ AI is responding!" -ForegroundColor Green
        Write-Host "   Response: $shortResponse..." -ForegroundColor Green
    } else {
        Write-Host "   ❌ No response from AI" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ AI test failed" -ForegroundColor Red
}

Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "✅ Health check complete!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Cyan