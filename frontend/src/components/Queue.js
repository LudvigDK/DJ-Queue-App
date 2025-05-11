import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Queue({ code, guest }) {
  const [items, setItems] = useState([]);

  const load = () => axios.get(`/events/${code}`).then(r => setItems(r.data.items));
  useEffect(() => { load(); const iv = setInterval(load, 5000); return ()=>clearInterval(iv); }, []);

  const vote = async (id) => {
    await axios.post(`/items/${id}/vote`);
    load();
  };

  return (
    <ul>
      {items.sort((a,b) => b.votes - a.votes).map(i => (
        <li key={i.id}>
          {i.title} – {i.artist} ({i.votes})
          {guest && <button onClick={()=>vote(i.id)}>▲</button>}
        </li>
      ))}
    </ul>
  );
}
