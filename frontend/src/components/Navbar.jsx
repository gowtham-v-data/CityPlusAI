/**
 * CityPulse AI — Navbar Component
 * Top navigation bar with city selector dropdown, live status, and connection indicator.
 */
import { useState, useRef, useEffect } from 'react';
import { FiWifi, FiWifiOff, FiClock, FiMapPin, FiChevronDown } from 'react-icons/fi';

export default function Navbar({ isConnected, activeCity, cities, onCityChange }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  const now = new Date().toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
  });

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleCitySelect = (cityId) => {
    onCityChange(cityId);
    setDropdownOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <div className="navbar-logo">🏙️</div>
        <div>
          <div className="navbar-title">CityPulse AI</div>
          <div className="navbar-subtitle">Real-Time City Monitoring</div>
        </div>
      </div>

      {/* City Selector */}
      <div className="city-selector-wrapper" ref={dropdownRef}>
        <button
          className="city-selector-btn"
          onClick={() => setDropdownOpen(!dropdownOpen)}
        >
          <FiMapPin size={14} />
          <span className="city-selector-name">
            {activeCity?.name || 'Select City'}
          </span>
          {activeCity?.state && (
            <span className="city-selector-state">{activeCity.state}</span>
          )}
          <FiChevronDown
            size={14}
            className={`city-selector-arrow ${dropdownOpen ? 'open' : ''}`}
          />
        </button>

        {dropdownOpen && (
          <div className="city-dropdown">
            <div className="city-dropdown-header">Select City to Monitor</div>
            {cities.map(city => (
              <button
                key={city.id}
                className={`city-dropdown-item ${activeCity?.id === city.id ? 'active' : ''}`}
                onClick={() => handleCitySelect(city.id)}
              >
                <div className="city-dropdown-info">
                  <span className="city-dropdown-name">{city.name}</span>
                  <span className="city-dropdown-state">{city.state}</span>
                </div>
                <span className="city-dropdown-zones">{city.zone_count} zones</span>
                {activeCity?.id === city.id && (
                  <span className="city-dropdown-active">●</span>
                )}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="navbar-status">
        <div className="status-badge">
          <FiClock size={12} />
          {now}
        </div>
        <div className="status-badge">
          <span className={`status-dot ${isConnected ? 'live' : 'offline'}`} />
          {isConnected ? 'Live' : 'Offline'}
        </div>
        <div className="status-badge">
          {isConnected ? <FiWifi size={12} /> : <FiWifiOff size={12} />}
          WebSocket
        </div>
      </div>
    </nav>
  );
}
