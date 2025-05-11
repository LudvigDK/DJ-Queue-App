import uuid, io, sqlite3
from datetime import datetime
import tidalapi, qrcode
from flask import (
    Flask, g, request, render_template,
    redirect, url_for, jsonify, send_file
)

app = Flask(__name__)
# configure your TIDAL credentials here
app.config['TIDAL_USERNAME'] = 'YOUR_TIDAL_USERNAME'
app.config['TIDAL_PASSWORD'] = 'YOUR_TIDAL_PASSWORD'

# --- DATABASE HELPERS ---
DB_PATH = 'database.db'
def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop('db', None)
    if db: db.close()

def init_db():
    db = get_db()
    db.execute("""
      CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        uuid TEXT UNIQUE,
        created_at TEXT
      )""")
    db.execute("""
      CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY,
        event_uuid TEXT,
        track_id TEXT,
        title TEXT,
        artist TEXT,
        votes INTEGER
      )""")
    db.commit()

# --- TIDAL SESSION ---
session = tidalapi.Session()
session.login(
    username=app.config['TIDAL_USERNAME'],
    password=app.config['TIDAL_PASSWORD']
)

# --- ROUTES ---
@app.before_first_request
def setup():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create_event():
    ev_uuid = uuid.uuid4().hex[:8]
    now = datetime.utcnow().isoformat()
    db = get_db()
    db.execute(
      "INSERT INTO events (uuid, created_at) VALUES (?, ?)",
      (ev_uuid, now)
    )
    db.commit()
    return redirect(url_for('dashboard', event_uuid=ev_uuid))

@app.route('/dashboard/<event_uuid>')
def dashboard(event_uuid):
    return render_template('dashboard.html', event_uuid=event_uuid)

@app.route('/qr/<event_uuid>.png')
def qr_code(event_uuid):
    url = url_for('event_page', event_uuid=event_uuid, _external=True)
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/event/<event_uuid>')
def event_page(event_uuid):
    return render_template('event.html', event_uuid=event_uuid)

@app.route('/api/<event_uuid>/search')
def search(event_uuid):
    q = request.args.get('q', '')
    results = session.search('track', q)
    out = []
    for t in results.tracks:
        out.append({
          'id': str(t.id),
          'title': t.name,
          'artist': t.artist.name
        })
    return jsonify(out)

@app.route('/api/<event_uuid>/add', methods=['POST'])
def add_track(event_uuid):
    data = request.json
    db = get_db()
    cur = db.execute(
      "SELECT 1 FROM tracks WHERE event_uuid=? AND track_id=?",
      (event_uuid, data['id'])
    )
    if cur.fetchone():
        return jsonify({'status':'exists'})
    db.execute(
      "INSERT INTO tracks (event_uuid, track_id, title, artist, votes) "
      "VALUES (?, ?, ?, ?, 0)",
      (event_uuid, data['id'], data['title'], data['artist'])
    )
    db.commit()
    return jsonify({'status':'ok'})

@app.route('/api/<event_uuid>/vote', methods=['POST'])
def vote(event_uuid):
    data = request.json
    db = get_db()
    db.execute(
      "UPDATE tracks SET votes=votes+1 WHERE event_uuid=? AND track_id=?",
      (event_uuid, data['id'])
    )
    db.commit()
    return jsonify({'status':'ok'})

@app.route('/api/<event_uuid>/queue')
def queue(event_uuid):
    db = get_db()
    cur = db.execute(
      "SELECT track_id, title, artist, votes "
      "FROM tracks WHERE event_uuid=? ORDER BY votes DESC",
      (event_uuid,)
    )
    tracks = [dict(r) for r in cur.fetchall()]
    return jsonify(tracks)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
