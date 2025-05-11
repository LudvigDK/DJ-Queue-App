import { useParams } from 'react-router-dom';
import Search from './Search';
import Queue from './Queue';

export default function GuestPage() {
  const { code } = useParams();
  return (
    <div className="p-4">
      <h1>Event: {code}</h1>
      <Search code={code} />
      <Queue code={code} guest />
    </div>
  );
}
