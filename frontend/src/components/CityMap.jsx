/**
 * CityPulse AI — City Map Component
 * Interactive Leaflet map that dynamically centers on the selected city.
 */
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import { useEffect } from 'react';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet default icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const DEFAULT_CENTER = [12.9716, 77.5946];
const MAP_ZOOM = 12;

/** Sub-component to fly the map to a new city center */
function MapFlyTo({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center && center.length === 2) {
      map.flyTo(center, MAP_ZOOM, { duration: 1.5 });
    }
  }, [center, map]);
  return null;
}

function getZoneStatus(zone) {
  if (zone.is_anomaly || zone.traffic_density > 85 || zone.aqi > 180) return 'danger';
  if (zone.traffic_density > 60 || zone.aqi > 120 || zone.power_consumption > 900) return 'warning';
  return 'normal';
}

function createZoneIcon(zone) {
  const status = getZoneStatus(zone);
  const colors = {
    normal: { bg: '#10b981', border: '#34d399' },
    warning: { bg: '#f59e0b', border: '#fbbf24' },
    danger: { bg: '#f43f5e', border: '#fb7185' },
  };
  const c = colors[status];

  return L.divIcon({
    className: '',
    html: `
      <div style="
        width: 34px; height: 34px;
        background: ${c.bg};
        border: 2px solid ${c.border};
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: white; font-weight: 700; font-size: 10px;
        font-family: 'JetBrains Mono', monospace;
        box-shadow: 0 2px 10px ${c.bg}66;
        ${status !== 'normal' ? `animation: markerGlow 2s infinite;` : ''}
      ">
        ${zone.zone_id.replace('zone_0', 'Z')}
      </div>
      <style>
        @keyframes markerGlow {
          0%, 100% { box-shadow: 0 0 0 0 ${c.bg}55; }
          50% { box-shadow: 0 0 0 12px ${c.bg}00; }
        }
      </style>
    `,
    iconSize: [34, 34],
    iconAnchor: [17, 17],
    popupAnchor: [0, -20],
  });
}

function ZonePopup({ zone }) {
  const status = getZoneStatus(zone);
  const statusColors = { normal: '#10b981', warning: '#f59e0b', danger: '#f43f5e' };

  return (
    <div className="zone-popup">
      <h3>{zone.zone_name}</h3>
      <div style={{
        display: 'inline-flex', alignItems: 'center', gap: '4px',
        padding: '2px 8px', borderRadius: '8px', fontSize: '0.65rem',
        fontWeight: 600, marginBottom: '8px',
        background: `${statusColors[status]}20`,
        color: statusColors[status],
      }}>
        ● {status.toUpperCase()}
      </div>

      <div className="zone-popup-row">
        <span className="zone-popup-label">🚗 Traffic</span>
        <span className="zone-popup-value">{zone.traffic_density?.toFixed(1)}%</span>
      </div>
      <div className="zone-popup-row">
        <span className="zone-popup-label">🌫️ AQI</span>
        <span className="zone-popup-value">{zone.aqi?.toFixed(1)}</span>
      </div>
      <div className="zone-popup-row">
        <span className="zone-popup-label">⚡ Power</span>
        <span className="zone-popup-value">{zone.power_consumption?.toFixed(0)} MW</span>
      </div>
      <div className="zone-popup-row">
        <span className="zone-popup-label">☀️ Solar</span>
        <span className="zone-popup-value">{zone.solar_generation?.toFixed(0)} MW</span>
      </div>
      <div className="zone-popup-row">
        <span className="zone-popup-label">🌡️ Temp</span>
        <span className="zone-popup-value">{zone.temperature?.toFixed(1)}°C</span>
      </div>
      <div className="zone-popup-row">
        <span className="zone-popup-label">💧 Humidity</span>
        <span className="zone-popup-value">{zone.humidity?.toFixed(1)}%</span>
      </div>
      {zone.is_anomaly && (
        <div style={{
          marginTop: '8px', padding: '4px 8px', borderRadius: '6px',
          background: 'rgba(244,63,94,0.15)', color: '#f43f5e',
          fontSize: '0.7rem', fontWeight: 600, textAlign: 'center',
        }}>
          ⚠️ ANOMALY DETECTED
        </div>
      )}
    </div>
  );
}

export default function CityMap({ zoneData, activeCity }) {
  const zones = zoneData || [];
  const mapCenter = activeCity?.center || DEFAULT_CENTER;

  return (
    <div className="panel map-panel">
      <div className="panel-header">
        <span className="panel-title">
          <span className="panel-title-icon">🗺️</span>
          City Zone Map
          {activeCity?.name && (
            <span style={{
              fontSize: '0.75rem',
              color: '#06b6d4',
              fontWeight: 400,
              marginLeft: '0.5rem',
            }}>
              — {activeCity.name}, {activeCity.state}
            </span>
          )}
        </span>
        <span className="panel-badge live">● Live Tracking</span>
      </div>
      <div className="map-container">
        <MapContainer
          center={mapCenter}
          zoom={MAP_ZOOM}
          scrollWheelZoom={true}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>'
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          />
          <MapFlyTo center={mapCenter} />
          {zones.map(zone => (
            <Marker
              key={zone.zone_id}
              position={[zone.latitude, zone.longitude]}
              icon={createZoneIcon(zone)}
            >
              <Popup>
                <ZonePopup zone={zone} />
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
