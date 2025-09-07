import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import { searhMovie, getDetails, getRecent } from './lib/api'


export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [recent, setRecent] = useState([]);
  const [details, setDetails] = useState(null);

  useEffect(() => {
    loadrecent();
  }, []);

  async function loadrecent() {
    try{
      setRecent(await getRecent());
    } catch (e){
      console.error(e);
    }
  }

  async function handleSearch(e) {
    e.preventDefault();
    if (!query.trim()) return;
    try {
      const data = await searhMovie(query);
      console.log('Search results:', data.results); // Debug log
      setResults(data.results || []);
    } catch (e) {
      console.error(e);
    }
    await loadrecent();
  }

  async function handleDetails(id) {
    try {
      const data = await getDetails(id);
      console.log('Movie details:', data); // Debug log
      setDetails(data);
    } catch (e) {
      console.error(e);
    }
  }



  return (
    <div style={{ padding: 20, maxWidth: 800, margin: '0 auto' }}>
      <h1>Movie Intelligence</h1>
      <form onSubmit={handleSearch} style={{ marginBottom: 20 }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for a movie..."
          style = {{width: "70%", padding:8}}
        />
        <button type = "submit" style = {{marginLeft: 8}}>Search</button> 
    
    </form>

    <h2>Search Results</h2>
    <ul>
      {results.map(movie => (
        <li key={movie.imdb_id}>
          {movie.title} ({movie.year})
          <button onClick={() => handleDetails(movie.imdb_id)} style={{ marginLeft: 8 }}>
            Details
          </button>
        </li>
      ))}
    </ul>

    <h2>Recent Searches</h2>
    <ul>
      {recent.map((t, i) => <li key={i}>{t}</li>)}
      </ul>

      {details && (
        <div style={{ marginTop: 20, padding: 10, border: '1px solid #ccc' }}>
          <h3>{details.title} ({details.year})</h3>
          {details.poster && details.poster !== 'N/A' && (
            <img src={details.poster} alt={details.title} style={{ maxWidth: 200, marginBottom: 10 }} />
          )}
          <p>{details.plot || "No plot available."}</p>
          <p>
            🎭 {details.genre || "N/A"} | 🎬 {details.director || "N/A"} | ⭐ {details.imdb_rating || "N/A"}
          </p>
        </div>
      )}

    </div>
  );
}


