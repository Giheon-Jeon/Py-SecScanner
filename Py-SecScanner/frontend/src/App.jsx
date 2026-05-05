import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({ xss: 0, sqli: 0, lfi: 0, paths: 0 });

  const addLog = (msg, type = 'info') => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [{ time, msg, type }, ...prev]);
  };

  const handleScan = () => {
    if (!url) return;
    
    setIsScanning(true);
    setLogs([]);
    setStats({ xss: 0, sqli: 0, lfi: 0, paths: 0 });
    
    addLog(`Scanning initiated for: ${url}`);
    
    // Simulate steps
    setTimeout(() => {
      addLog("Discovering forms and input fields...");
      setStats(prev => ({ ...prev, paths: 12 }));
    }, 1000);

    setTimeout(() => {
      addLog("Injecting XSS payloads...", "info");
    }, 2500);

    setTimeout(() => {
      addLog("Vulnerability detected: Reflected XSS at /login", "warn");
      setStats(prev => ({ ...prev, xss: 1 }));
    }, 4000);

    setTimeout(() => {
      addLog("Testing SQL Injection vectors...");
    }, 5500);

    setTimeout(() => {
      addLog("Scan complete. Generating report.", "success");
      setIsScanning(false);
    }, 8000);
  };

  return (
    <div className="app-container">
      <header>
        <h1>Py-SecScanner 2.0</h1>
        <p>Advanced Security Vulnerability Assessment Tool</p>
      </header>

      <div className="search-section">
        <div className="search-box glass">
          <input 
            type="text" 
            placeholder="Enter Target URL (e.g., https://example.com)" 
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={isScanning}
          />
          <button 
            className="scan-btn" 
            onClick={handleScan}
            disabled={isScanning}
          >
            {isScanning ? 'Scanning...' : 'Scan Now'}
          </button>
        </div>
      </div>

      <div className={`dashboard ${isScanning || logs.length > 0 ? 'active' : ''}`}>
        <div className="card glass danger">
          <h3>XSS Detected</h3>
          <div className="value">{stats.xss}</div>
        </div>
        <div className="card glass danger">
          <h3>SQL Injection</h3>
          <div className="value">{stats.sqli}</div>
        </div>
        <div className="card glass info">
          <h3>LFI / Path Traversal</h3>
          <div className="value">{stats.lfi}</div>
        </div>
        <div className="card glass success">
          <h3>Forms Discovered</h3>
          <div className="value">{stats.paths}</div>
        </div>
      </div>

      {(isScanning || logs.length > 0) && (
        <div className="status-log glass">
          {logs.map((log, i) => (
            <div key={i} className="log-entry">
              <span className="log-time">[{log.time}]</span>
              <span className={`log-msg ${log.type === 'warn' ? 'warn' : ''}`}>
                {log.msg}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
