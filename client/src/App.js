import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [events, setEvents] = useState([]);
  const seenIds = useRef(new Set());

  const fetchEvents = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/api/events");
      const now = new Date();

      const fresh = res.data.filter((event) => {
        const id = event.request_id;
        const timestamp = new Date(event.timestamp);
        const ageInSeconds = (now - timestamp) / 1000;

        // Keep events that are new AND within 90 seconds
        return (
          id &&
          !seenIds.current.has(id) &&
          ageInSeconds >= 0 && // skip future timestamps
          ageInSeconds <= 90 // max age = 90 seconds
        );
      });

      fresh.forEach((e) => seenIds.current.add(e.request_id));
      setEvents((prev) => [...fresh, ...prev]); // append only fresh events
    } catch (err) {
      console.error("Error fetching events:", err);
    }
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 15000); // poll every 15 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h2>GitHub Webhook Events</h2>
      {events.length === 0 && <p>No recent events</p>}
      {events.map((event, index) => (
        <div key={event.request_id || index} className="event-card">
          <p>{event.message}</p>
          <small>{event.timestamp}</small>
        </div>
      ))}
    </div>
  );
}

export default App;
