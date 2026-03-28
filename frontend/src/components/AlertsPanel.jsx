/**
 * CityPulse AI — Alerts Panel Component
 * Real-time alert notifications with severity-based styling.
 */
import {
  FiAlertTriangle,
  FiAlertOctagon,
  FiInfo,
  FiAlertCircle,
} from 'react-icons/fi';

const severityIcons = {
  critical: <FiAlertOctagon />,
  high: <FiAlertTriangle />,
  medium: <FiAlertCircle />,
  low: <FiInfo />,
};

function formatTime(timestamp) {
  if (!timestamp) return '';
  try {
    const d = new Date(timestamp);
    return d.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true,
    });
  } catch {
    return timestamp;
  }
}

export default function AlertsPanel({ alerts }) {
  return (
    <div className="panel">
      <div className="panel-header">
        <span className="panel-title">
          <span className="panel-title-icon">🔔</span>
          Alerts & Warnings
        </span>
        <span className="panel-badge live">
          {alerts.length > 0 ? `${alerts.length} alerts` : 'Clear'}
        </span>
      </div>
      <div className="panel-body">
        {alerts.length === 0 ? (
          <div className="no-alerts">
            <div className="no-alerts-icon">✅</div>
            <p>All systems operating normally</p>
            <p style={{ fontSize: '0.7rem', marginTop: '0.25rem' }}>
              No threshold violations detected
            </p>
          </div>
        ) : (
          <div className="alerts-list">
            {alerts.slice(0, 20).map((alert, idx) => (
              <div
                key={`${alert.zone_id}-${alert.category}-${idx}`}
                className={`alert-item ${alert.severity || 'medium'}`}
              >
                <div className={`alert-severity-icon ${alert.severity || 'medium'}`}>
                  {severityIcons[alert.severity] || <FiInfo />}
                </div>
                <div className="alert-content">
                  <div className="alert-message">
                    {alert.message || 'Threshold exceeded'}
                  </div>
                  <div className="alert-meta">
                    <span className={`alert-category-tag ${alert.category || ''}`}>
                      {alert.category || 'general'}
                    </span>
                    <span>{formatTime(alert.timestamp)}</span>
                    <span>{alert.zone_name || ''}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
