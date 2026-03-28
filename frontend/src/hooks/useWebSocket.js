/**
 * CityPulse AI — WebSocket Hook
 * Manages real-time connection to the FastAPI backend.
 * Supports city switching via WebSocket messages.
 */
import { useState, useEffect, useRef, useCallback } from 'react';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const RECONNECT_DELAY = 3000;
const PING_INTERVAL = 25000;

export function useWebSocket() {
  const [isConnected, setIsConnected] = useState(false);
  const [zoneData, setZoneData] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [historyData, setHistoryData] = useState([]);
  const [activeCity, setActiveCity] = useState(null);
  const [cities, setCities] = useState([]);
  const wsRef = useRef(null);
  const reconnectTimerRef = useRef(null);
  const pingTimerRef = useRef(null);
  const maxHistory = 30;

  // Fetch available cities on mount
  useEffect(() => {
    fetch(`${API_URL}/cities`)
      .then(res => res.json())
      .then(data => setCities(data))
      .catch(err => console.warn('Failed to fetch cities:', err));
  }, []);

  const switchCity = useCallback((cityId) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(`city:${cityId}`);
      // Clear history on city switch for fresh charts
      setHistoryData([]);
      setAlerts([]);
    }
  }, []);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    try {
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('🔗 Connected to CityPulse AI');
        setIsConnected(true);
        pingTimerRef.current = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send('ping');
          }
        }, PING_INTERVAL);
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);

          if (message.type === 'initial_snapshot' || message.type === 'sensor_update' || message.type === 'city_changed') {
            const zones = message.zones || [];
            setZoneData(zones);

            // Update active city info
            if (message.city) {
              setActiveCity(message.city);
            }

            // On city change, reset history
            if (message.type === 'city_changed') {
              setHistoryData([]);
              setAlerts([]);
            }

            // Accumulate history for charts
            if (zones.length > 0) {
              setHistoryData(prev => {
                const newPoint = {
                  timestamp: new Date().toLocaleTimeString('en-US', {
                    hour12: false,
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                  }),
                  ...zones.reduce((acc, z) => ({
                    avgTraffic: (acc.avgTraffic || 0) + z.traffic_density / zones.length,
                    avgAqi: (acc.avgAqi || 0) + z.aqi / zones.length,
                    totalEnergy: (acc.totalEnergy || 0) + z.power_consumption,
                    totalSolar: (acc.totalSolar || 0) + (z.solar_generation || 0),
                  }), {}),
                };
                const updated = [...prev, newPoint];
                return updated.slice(-maxHistory);
              });
            }

            // Accumulate alerts
            if (message.alerts && message.alerts.length > 0) {
              setAlerts(prev => {
                const newAlerts = [...message.alerts, ...prev];
                return newAlerts.slice(0, 100);
              });
            }
          }
        } catch (err) {
          console.warn('Failed to parse WS message:', err);
        }
      };

      ws.onclose = () => {
        console.log('🔌 Disconnected from CityPulse AI');
        setIsConnected(false);
        clearInterval(pingTimerRef.current);
        reconnectTimerRef.current = setTimeout(connect, RECONNECT_DELAY);
      };

      ws.onerror = (err) => {
        console.error('WebSocket error:', err);
        ws.close();
      };

    } catch (err) {
      console.error('Connection failed:', err);
      reconnectTimerRef.current = setTimeout(connect, RECONNECT_DELAY);
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      clearTimeout(reconnectTimerRef.current);
      clearInterval(pingTimerRef.current);
      if (wsRef.current) wsRef.current.close();
    };
  }, [connect]);

  return { isConnected, zoneData, alerts, historyData, activeCity, cities, switchCity };
}
