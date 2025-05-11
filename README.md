# DJ Queue Dashboard

## Setup Backend

```bash
cd backend
pip install -r requirements.txt
export TIDAL_API_KEY=your_key
uvicorn app.main:app --reload
```

## Setup Frontend

```bash
cd frontend
npm install
npm start
```

Guests visit `/guest/<event_code>`, DJs use `/dashboard?code=<event_code>`.
