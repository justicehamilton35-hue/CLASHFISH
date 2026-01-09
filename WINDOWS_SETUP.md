# ClashFish Setup for Windows 🪟

Complete guide for setting up ClashFish on Windows with PowerShell.

---

## Quick Start (5 Minutes)

### Step 1: Setup API Key

Open **PowerShell** in the ClashFish directory and run:

```powershell
.\scripts\setup_api_key.ps1
```

When prompted, paste your Clash Royale API key.

### Step 2: Test API Key

```powershell
.\scripts\test_api_key.ps1
```

You should see: **✅ SUCCESS! API key is working correctly**

### Step 3: Start ClashFish

```powershell
.\scripts\start_dev.ps1
```

### Step 4: Open Your Browser

Visit: **http://localhost:8000**

Search for any player tag! 🎮

---

## Prerequisites

### Required:
- **Python 3.10+** - Download from [python.org](https://www.python.org/downloads/)
- **Git** - You already have this!
- **PowerShell** - Built into Windows 10/11

### Optional:
- **PostgreSQL 14+** - Only if not using mock data
- **Docker Desktop** - For full-stack deployment

---

## PowerShell Commands

### Important: Running Scripts on Windows

Windows PowerShell requires `.\` prefix to run scripts in the current directory:

```powershell
# ✅ Correct (with .\ prefix)
.\scripts\setup_api_key.ps1
.\scripts\test_api_key.ps1
.\scripts\start_dev.ps1

# ❌ Wrong (missing .\ prefix)
scripts/setup_api_key.ps1     # Won't work
/scripts/test_api_key.sh       # Wrong - this is a bash script
```

### Execution Policy Error?

If you get an error about execution policy, run PowerShell **as Administrator** and execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try again.

---

## Step-by-Step Setup

### 1. Check Python Installation

```powershell
python --version
```

Should show `Python 3.10.0` or higher.

If not installed:
1. Download from [python.org](https://www.python.org/downloads/)
2. **Check "Add Python to PATH"** during installation
3. Restart PowerShell
4. Try again

### 2. Navigate to ClashFish Directory

```powershell
cd G:\ClashFish
# Or wherever you cloned the repo
```

### 3. Get Your Clash Royale API Key

1. Go to https://developer.clashroyale.com
2. Log in with your Supercell ID
3. Create a new API key
4. **Important**: Whitelist your IP address

**Find your IP:**
```powershell
(Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing).Content
```

### 4. Configure ClashFish

**Option A: Automated (Recommended)**

```powershell
.\scripts\setup_api_key.ps1
```

**Option B: Manual**

```powershell
# Copy template
Copy-Item .env.example .env

# Edit .env in notepad
notepad .env

# Update these lines:
CLASH_ROYALE_API_KEY=your_api_key_here
USE_MOCK_DATA=false
```

### 5. Test Your Setup

```powershell
.\scripts\test_api_key.ps1
```

**Expected output:**
```
✅ SUCCESS! API key is working correctly
📊 Player data received:
   Name: Surgical Goblin
   Tag: #2PP
   Trophies: 8000
```

### 6. Start ClashFish

```powershell
.\scripts\start_dev.ps1
```

This will:
- Create a virtual environment (if needed)
- Install all dependencies
- Start the web server

### 7. Access the Dashboard

Open your browser to: **http://localhost:8000**

---

## Alternative: Using Git Bash

If you have Git for Windows, you can use Git Bash to run the `.sh` scripts:

```bash
# Open Git Bash (right-click → Git Bash Here)
./scripts/setup_api_key.sh
./scripts/test_api_key.sh
./scripts/start_dev.sh
```

---

## Alternative: Using WSL (Windows Subsystem for Linux)

If you have WSL installed:

```bash
# Open WSL terminal
cd /mnt/g/ClashFish  # Adjust path as needed

./scripts/setup_api_key.sh
./scripts/test_api_key.sh
./scripts/start_dev.sh
```

---

## Troubleshooting

### "Script cannot be loaded" Error

**Error:**
```
.\scripts\setup_api_key.ps1 : File cannot be loaded because running scripts is disabled on this system.
```

**Fix:**
Run PowerShell **as Administrator**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Python not found" Error

**Fix:**
1. Install Python from python.org
2. **Check "Add Python to PATH"** during installation
3. Restart PowerShell
4. Verify: `python --version`

### "pip not found" Error

**Fix:**
```powershell
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### "Access denied (403)" from API

**Fix:**
Your IP is not whitelisted.

```powershell
# Get your current IP
(Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing).Content

# Add this IP at developer.clashroyale.com
# Wait 2-3 minutes
# Test again
.\scripts\test_api_key.ps1
```

### Port 8000 already in use

**Fix:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use a different port
cd backend
python -m uvicorn main:app --port 8001
```

### Virtual environment activation fails

**Fix:**
```powershell
# Delete old venv
Remove-Item -Recurse -Force venv

# Create new one
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1
```

### Dependencies won't install

**Fix:**
```powershell
# Upgrade pip first
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r backend\requirements.txt

# If specific package fails, install manually
pip install package-name
```

---

## File Paths on Windows

Windows uses backslashes (`\`) instead of forward slashes (`/`):

```powershell
# ✅ Correct
.\scripts\start_dev.ps1
backend\requirements.txt
data\mock\sample_player.json

# ⚠️ Also works (PowerShell accepts both)
./scripts/start_dev.ps1
backend/requirements.txt
data/mock/sample_player.json
```

---

## Environment Variables

### View current .env settings:

```powershell
Get-Content .env
```

### Edit .env file:

```powershell
notepad .env
# or
code .env  # If you have VS Code
```

### Quick toggle between modes:

**Use Mock Data (no API needed):**
```powershell
(Get-Content .env) -replace 'USE_MOCK_DATA=false', 'USE_MOCK_DATA=true' | Set-Content .env
```

**Use Real API:**
```powershell
(Get-Content .env) -replace 'USE_MOCK_DATA=true', 'USE_MOCK_DATA=false' | Set-Content .env
```

---

## Running Tests

Once the server is running, you can test it:

```powershell
# In a new PowerShell window

# Test health endpoint
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/health" -UseBasicParsing

# Get player data
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/players/2PP" -UseBasicParsing
```

---

## Next Steps

Once everything is working:

1. **Analyze Players**: Search any player tag at http://localhost:8000
2. **Explore API**: Visit http://localhost:8000/docs for API documentation
3. **Build Features**: Start implementing win probability, move evaluation, etc.
4. **Deploy**: When ready, deploy to a cloud service

---

## Quick Command Reference

```powershell
# Setup
.\scripts\setup_api_key.ps1          # Configure API key
.\scripts\test_api_key.ps1           # Test API connection
.\scripts\start_dev.ps1              # Start server

# Utilities
python --version                      # Check Python version
pip list                              # Show installed packages
Get-Content .env                      # View configuration

# Manual operations
python -m venv venv                   # Create virtual env
.\venv\Scripts\Activate.ps1          # Activate venv
pip install -r backend\requirements.txt  # Install dependencies
cd backend                            # Go to backend folder
python -m uvicorn main:app --reload  # Start server manually
```

---

## Development with VS Code (Optional)

If you use Visual Studio Code:

1. **Open ClashFish folder in VS Code**
2. **Install Python extension** (Microsoft)
3. **Select Python interpreter**: `Ctrl+Shift+P` → "Python: Select Interpreter" → Choose `.\venv\Scripts\python.exe`
4. **Open integrated terminal**: `` Ctrl+` ``
5. **Run scripts** directly in VS Code terminal

---

## Docker on Windows (Optional)

If you have Docker Desktop:

```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

---

## Summary

| Task | Command |
|------|---------|
| Setup API | `.\scripts\setup_api_key.ps1` |
| Test API | `.\scripts\test_api_key.ps1` |
| Start Server | `.\scripts\start_dev.ps1` |
| View .env | `Get-Content .env` |
| Edit .env | `notepad .env` |
| Check IP | `(Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing).Content` |

---

## Need Help?

- **Setup Issues**: See this guide (WINDOWS_SETUP.md)
- **API Issues**: See API_SETUP.md
- **General Help**: See QUICKSTART.md
- **Full Documentation**: See DESIGN.md

---

**You're all set!** Start analyzing Clash Royale players on Windows! 🎮🪟
