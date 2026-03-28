/**
 * CityPulse AI — Zone Table Component
 * Tabular view of all city zones with real-time metrics.
 */

function getTrafficClass(val) {
  if (val > 75) return 'bad';
  if (val > 50) return 'moderate';
  return 'good';
}

function getAqiClass(val) {
  if (val > 150) return 'bad';
  if (val > 100) return 'moderate';
  return 'good';
}

function getStatus(zone) {
  if (zone.is_anomaly || zone.traffic_density > 85 || zone.aqi > 180) return 'danger';
  if (zone.traffic_density > 60 || zone.aqi > 120) return 'warning';
  return 'normal';
}

const statusLabels = {
  normal: 'Normal',
  warning: 'Warning',
  danger: 'Critical',
};

export default function ZoneTable({ zoneData }) {
  const zones = zoneData || [];

  return (
    <div className="panel" style={{ gridColumn: '1 / -1' }}>
      <div className="panel-header">
        <span className="panel-title">
          <span className="panel-title-icon">📊</span>
          Zone Overview
        </span>
        <span className="panel-badge live">{zones.length} zones</span>
      </div>
      <div className="panel-body" style={{ padding: '0' }}>
        <div className="zone-table-container">
          <table className="zone-table">
            <thead>
              <tr>
                <th>Zone</th>
                <th>Traffic</th>
                <th>AQI</th>
                <th>Power (MW)</th>
                <th>Solar (MW)</th>
                <th>Temp</th>
                <th>Speed (km/h)</th>
                <th>AI Prediction</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {zones.length === 0 ? (
                <tr>
                  <td colSpan={9} style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
                    Waiting for data...
                  </td>
                </tr>
              ) : (
                zones.map(zone => {
                  const status = getStatus(zone);
                  return (
                    <tr key={zone.zone_id}>
                      <td className="zone-name-cell">{zone.zone_name}</td>
                      <td className={`value-cell ${getTrafficClass(zone.traffic_density)}`}>
                        {zone.traffic_density?.toFixed(1)}%
                      </td>
                      <td className={`value-cell ${getAqiClass(zone.aqi)}`}>
                        {zone.aqi?.toFixed(1)}
                      </td>
                      <td className="value-cell">
                        {zone.power_consumption?.toFixed(0)}
                      </td>
                      <td className="value-cell" style={{ color: '#10b981' }}>
                        {zone.solar_generation?.toFixed(0)}
                      </td>
                      <td className="value-cell">
                        {zone.temperature?.toFixed(1)}°C
                      </td>
                      <td className="value-cell">
                        {zone.avg_speed?.toFixed(1)}
                      </td>
                      <td className="value-cell" style={{ color: '#8b5cf6' }}>
                        T:{zone.predicted_traffic?.toFixed(0)}%
                        {' '}A:{zone.predicted_aqi?.toFixed(0)}
                      </td>
                      <td>
                        <span className={`status-pill ${status}`}>
                          <span style={{
                            width: '6px', height: '6px',
                            borderRadius: '50%',
                            background: 'currentColor',
                            display: 'inline-block',
                          }} />
                          {statusLabels[status]}
                        </span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
