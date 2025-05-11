import { useState } from 'react';
import axios from 'axios';

export default function Search({ code }) {
  const [q, setQ] = useState('');
  const [results, setResults] = useState([]);

  const find = async () => {
    const r = await axios.get(`/search/`, { params: { q } });
    setResults(r.data);
  };

  const add = async (item) => {
    await axios.post(`/events/${code}/items/`, item);
  };

  return (
    <div>
      <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search Tidal" />
      <button onClick={find}>Search</button>
      <ul>
        {results.map(i => (
          <li key={i.track_id}>
            {i.title} – {i.artist}
            <button onClick={()=>add(i)}>Add</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
