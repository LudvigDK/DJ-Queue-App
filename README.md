# DJ Queue Dashboard (SQLite, FastAPI + Flask)

## Setup

1. **Backend**  
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   - Uses local `dj_queue.db` SQLite file.

2. **Frontend**  
   ```bash
   cd flask_frontend
   pip install -r requirements.txt
   python app.py
   ```
   - Browse `http://localhost:5000` to create events and guests use the same server.

3. **Tidal**  
   - Set `TIDAL_API_KEY` env var if you want search to work:
     ```bash
     export TIDAL_API_KEY=your_access_token
     ```

No external DB—everything runs with Python and a local SQLite file.