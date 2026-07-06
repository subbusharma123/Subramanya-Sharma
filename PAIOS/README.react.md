# PAIOS React Dashboard

This repo now includes a React frontend for the PAIOS dashboard, served separately from the backend API.

## Start the backend

```powershell
python -m pip install -r requirements.txt
python -m uvicorn core.api:app --reload --port 8000
```

## Start the frontend

```powershell
npm install
npm start
```

## Notes

- React app runs on `http://localhost:3000`
- Backend API runs on `http://localhost:8000`
- The frontend fetches summary data from `/api/home` and `/api/projects`
