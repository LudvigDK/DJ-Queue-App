import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function App() {
  const [name, setName] = useState('');
  const nav = useNavigate();

  const create = async () => {
    const res = await axios.post('/events/', { name });
    nav(`/dashboard?code=${res.data.code}`);
  };

  return (
    <div className="p-4">
      <h1>Create Event</h1>
      <input value={name} onChange={e=>setName(e.target.value)} placeholder="Event name" />
      <button onClick={create}>Start</button>
    </div>
  );
}
