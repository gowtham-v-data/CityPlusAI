/**
 * CityPulse AI — Traffic Chart Component
 * Real-time traffic density line chart using Recharts.
 */
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: 'rgba(17, 24, 39, 0.95)',
      border: '1px solid rgba(255,255,255,0.1)',
      borderRadius: '8px',
      padding: '10px 14px',
      fontSize: '0.75rem',
      fontFamily: 'Inter, sans-serif',
    }}>
      <p style={{ color: '#94a3b8', marginBottom: '4px' }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color, fontWeight: 600 }}>
          {p.name}: {p.value?.toFixed(1)}{p.name.includes('Traffic') ? '%' : ''}
        </p>
      ))}
    </div>
  );
};

export default function TrafficChart({ historyData }) {
  return (
    <div className="panel">
      <div className="panel-header">
        <span className="panel-title">
          <span className="panel-title-icon">🚗</span>
          Traffic Density
        </span>
        <span className="panel-badge live">● Live</span>
      </div>
      <div className="panel-body">
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={historyData} margin={{ top: 5, right: 10, left: -10, bottom: 0 }}>
              <defs>
                <linearGradient id="trafficGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis
                dataKey="timestamp"
                stroke="#64748b"
                fontSize={10}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                stroke="#64748b"
                fontSize={10}
                tickLine={false}
                axisLine={false}
                domain={[0, 100]}
                tickFormatter={v => `${v}%`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="avgTraffic"
                name="Avg Traffic"
                stroke="#3b82f6"
                fill="url(#trafficGrad)"
                strokeWidth={2}
                dot={false}
                animationDuration={300}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
