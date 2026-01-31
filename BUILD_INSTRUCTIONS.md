# Build Instructions for Jordan Vectorizer

## Prerequisites

### Windows

1. **Install Visual Studio Build Tools 2017 or later**
   - Download from: https://visualstudio.microsoft.com/downloads/
   - Select "Desktop development with C++" workload
   - Or install via command line:
   ```powershell
   # Using winget
   winget install Microsoft.VisualStudio.2022.BuildTools
   
   # Or using Chocolatey
   choco install visualstudio2022buildtools --package-parameters "--add Microsoft.VisualStudio.Workload.VCTools"
   ```

2. **Install Rust**
   ```powershell
   # Download and run rustup-init.exe from https://rustup.rs/
   # Or use winget
   winget install Rustlang.Rustup
   ```

3. **Install Node.js 20+**
   ```powershell
   winget install OpenJS.NodeJS.LTS
   ```

### Linux/Mac

1. **Install Rust**
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

2. **Install Node.js 20+**
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt-get install -y nodejs
   
   # macOS
   brew install node@20
   ```

3. **Install build tools**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install build-essential
   
   # macOS (Xcode Command Line Tools)
   xcode-select --install
   ```

---

## Building the Project

### Step 1: Install Dependencies
```bash
npm install
```

### Step 2: Build the Native Module
```bash
npm run build
```

This will compile the Rust code and create the native Node.js module (`.node` file).

### Step 3: Verify Build
```bash
# Test the CLI
node cli/index.mjs testing_images/Little_Coffee_Buddy-29180-PNGVerse.png output.svg
```

---

## Quick Build (Windows)

```powershell
# Install prerequisites (run as Administrator)
winget install Microsoft.VisualStudio.2022.BuildTools
winget install Rustlang.Rustup
winget install OpenJS.NodeJS.LTS

# Restart PowerShell to refresh PATH

# Build the project
cd d:\vectorizer-main\vectorizer-main
npm install
npm run build

# Start the API
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

---

## Troubleshooting

### Error: "linker `link.exe` not found"
**Solution:** Install Visual Studio Build Tools with C++ workload.

### Error: "Cannot find module '@neplex/vectorizer-win32-x64-msvc'"
**Solution:** Run `npm run build` to compile the native module.

### Error: "cargo: command not found"
**Solution:** Install Rust using rustup and restart your terminal.

---

## Alternative: Use Pre-built Docker Image

If you don't want to build locally, use the pre-built Docker image:

```bash
docker pull igabhix001/jordan-vectorizer:latest
docker run -p 8000:8000 igabhix001/jordan-vectorizer:latest
```

---

## For Development

```bash
# Build in debug mode (faster compilation)
npm run build:debug

# Run tests
npm test

# Run benchmarks
npm run benchmark
```
