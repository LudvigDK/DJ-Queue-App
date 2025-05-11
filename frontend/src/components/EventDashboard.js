import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import axios from 'axios';
import QRCode from 'qrcode.react';
import Queue from './Queue';

export default function EventDashboard() {
  const [params] = useSearchParams();
  const code = params.get('code');
  const [event, setEvent] = useState(null);
  const link = `${window.location.origin}/guest/${code}`;

  useEffect(() => {
    axios.get(`/events/${code}`).then(r => setEvent(r.data));
  }, [code]);

  return (
    <div className="p-4">
      <h1>Dashboard: {event?.name}</h1>
      <QRCode value={link} />
      <p>Share link: <a href={link}>{link}</a></p>
      <Queue code={code} />
    </div>
  );
}
