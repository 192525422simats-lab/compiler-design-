# Disaster Relief DRL Compiler Web App

Academic implementation based on your PPT: **Compiler-Based Disaster Relief Resource Allocation for Faster and Accurate Emergency Response**.

## Run in VS Code (Windows)
1. Install Python 3.10+ (https://www.python.org/downloads/) and VS Code (https://code.visualstudio.com/). Enable **Add Python to PATH** during Python installation.
2. Extract this ZIP, open VS Code → File → Open Folder → `disaster_relief_drl`.
3. Open Terminal → New Terminal.
4. Create environment: `py -m venv .venv`
5. Activate:
   - PowerShell: `.venv\\Scripts\\Activate.ps1`
   - CMD: `.venv\\Scripts\\activate.bat`
   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again.
6. Install: `python -m pip install --upgrade pip` then `pip install -r requirements.txt`
7. Run: `python app.py`
8. Open http://127.0.0.1:5000. Keep terminal running; stop with Ctrl+C.

## Demo login
Email: `demo@relief.local` | Password: `Demo@123`. Or create your own account.

## DRL statement formats
`DISASTER TYPE AT "LOCATION" PRIORITY HIGH;`
`RESOURCE WATER 500;`
`ALLOCATE WATER 200 TO "LOCATION";`

Priorities: HIGH, MEDIUM, LOW. Resources: WATER, FOOD, MEDICAL_KIT, SHELTER, BLANKET, RESCUE_BOAT, MEDICINE. Allocations must be positive, within declared stock, and use the disaster destination.

## Project files
`app.py` Flask routes/auth/database; `compiler.py` six-phase compiler; `templates/` pages; `static/css/style.css` UI; `requirements.txt`.

**Important:** This is an academic simulation, not a live emergency dispatch service. It does not connect to emergency agencies, GPS or live data. For deployment, change the secret key and disable debug mode.
