# DJ Queue Dashboard (FastAPI + Flask Frontend)

## Setup Backend

```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:pass@host:port/dbname
export TIDAL_API_KEY=<your_access_token>
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Setup Flask Frontend

```bash
cd flask_frontend
pip install -r requirements.txt
# Set this to point at your running FastAPI
export API_BASE=http://localhost:8000
python app.py
```

- FastAPI runs on port 8000
- Flask frontend runs on port 5000
- Visit http://localhost:5000 to create events, view dashboards, search/vote
