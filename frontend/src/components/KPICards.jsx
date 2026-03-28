/**
 * CityPulse AI — KPI Cards Component
 * Displays key performance indicators with animated values.
 */
import {
  FiTruck,
  FiWind,
  FiZap,
  FiAlertTriangle,
  FiSun,
  FiActivity,
} from 'react-icons/fi';

export default function KPICards({ zoneData, alertCount }) {
  if (!zoneData || zoneData.length === 0) {
    return (
      <div className="kpi-grid">
        {['traffic', 'pollution', 'energy', 'alerts', 'solar', 'anomaly'].map(type => (
          <div key={type} className={`kpi-card ${type}`}>
            <div className={`kpi-icon ${type}`}>
              {type === 'traffic' && <FiTruck />}
              {type === 'pollution' && <FiWind />}
              {type === 'energy' && <FiZap />}
              {type === 'alerts' && <FiAlertTriangle />}
              {type === 'solar' && <FiSun />}
              {type === 'anomaly' && <FiActivity />}
            </div>
            <div className="kpi-info">
              <div className="kpi-label">{type}</div>
              <div className={`kpi-value ${type}`}>--</div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  const zones = zoneData;
  const avgTraffic = zones.reduce((s, z) => s + (z.traffic_density || 0), 0) / zones.length;
  const avgAqi = zones.reduce((s, z) => s + (z.aqi || 0), 0) / zones.length;
  const totalEnergy = zones.reduce((s, z) => s + (z.power_consumption || 0), 0);
  const totalSolar = zones.reduce((s, z) => s + (z.solar_generation || 0), 0);
  const anomalyCount = zones.filter(z => z.is_anomaly).length;

  return (
    <div className="kpi-grid">
      <div className="kpi-card traffic">
        <div className="kpi-icon traffic"><FiTruck /></div>
        <div className="kpi-info">
          <div className="kpi-label">Avg Traffic</div>
          <div className="kpi-value traffic">
            {avgTraffic.toFixed(1)}<span className="kpi-unit">%</span>
          </div>
          <div className={`kpi-change ${avgTraffic > 60 ? 'up' : 'down'}`}>
            {avgTraffic > 60 ? '▲ High' : '▼ Normal'}
          </div>
        </div>
      </div>

      <div className="kpi-card pollution">
        <div className="kpi-icon pollution"><FiWind /></div>
        <div className="kpi-info">
          <div className="kpi-label">Avg AQI</div>
          <div className="kpi-value pollution">
            {avgAqi.toFixed(1)}<span className="kpi-unit">idx</span>
          </div>
          <div className={`kpi-change ${avgAqi > 100 ? 'up' : 'down'}`}>
            {avgAqi > 150 ? '▲ Unhealthy' : avgAqi > 100 ? '▲ Moderate' : '▼ Good'}
          </div>
        </div>
      </div>

      <div className="kpi-card energy">
        <div className="kpi-icon energy"><FiZap /></div>
        <div className="kpi-info">
          <div className="kpi-label">Total Power</div>
          <div className="kpi-value energy">
            {totalEnergy.toFixed(0)}<span className="kpi-unit">MW</span>
          </div>
          <div className={`kpi-change ${totalEnergy > 3000 ? 'up' : 'down'}`}>
            {totalEnergy > 3000 ? '▲ Peak Load' : '▼ Normal'}
          </div>
        </div>
      </div>

      <div className="kpi-card alerts">
        <div className="kpi-icon alerts"><FiAlertTriangle /></div>
        <div className="kpi-info">
          <div className="kpi-label">Active Alerts</div>
          <div className="kpi-value alerts">{alertCount}</div>
          <div className={`kpi-change ${alertCount > 3 ? 'up' : 'down'}`}>
            {alertCount > 3 ? '▲ Attention!' : '▼ Stable'}
          </div>
        </div>
      </div>

      <div className="kpi-card traffic">
        <div className="kpi-icon solar"><FiSun /></div>
        <div className="kpi-info">
          <div className="kpi-label">Solar Generation</div>
          <div className="kpi-value solar">
            {totalSolar.toFixed(0)}<span className="kpi-unit">MW</span>
          </div>
          <div className="kpi-change down">
            {((totalSolar / Math.max(totalEnergy, 1)) * 100).toFixed(1)}% of load
          </div>
        </div>
      </div>

      <div className="kpi-card alerts">
        <div className="kpi-icon anomaly"><FiActivity /></div>
        <div className="kpi-info">
          <div className="kpi-label">Anomalies</div>
          <div className="kpi-value anomaly">{anomalyCount}</div>
          <div className={`kpi-change ${anomalyCount > 0 ? 'up' : 'down'}`}>
            {anomalyCount > 0 ? '▲ Detected' : '▼ None'}
          </div>
        </div>
      </div>
    </div>
  );
}
