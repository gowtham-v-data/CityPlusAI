/**
 * CityPulse AI — AQI Chart Component
 * Real-time Air Quality Index visualization.
 */
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
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
    }}>
      <p style={{ color: '#94a3b8', marginBottom: '4px' }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color, fontWeight: 600 }}>
          {p.name}: {p.value?.toFixed(1)}
        </p>
      ))}
    </div>
  );
};

export default function AQIChart({ historyData }) {
  return (
    <div className="panel">
      <div className="panel-header">
        <span className="panel-title">
          <span className="panel-title-icon">🌫️</span>
          Air Quality Index
        </span>
        <span className="panel-badge ai">AI Predicted</span>
      </div>
      <div className="panel-body">
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={historyData} margin={{ top: 5, right: 10, left: -10, bottom: 0 }}>
              <defs>
                <linearGradient id="aqiGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
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
                domain={[0, 'auto']}
              />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine
                y={150}
                stroke="#f43f5e"
                strokeDasharray="5 5"
                strokeOpacity={0.5}
                label={{
                  value: 'Danger',
                  position: 'insideTopRight',
                  fill: '#f43f5e',
                  fontSize: 10,
                }}
              />
              <Area
                type="monotone"
                dataKey="avgAqi"
                name="Avg AQI"
                stroke="#f59e0b"
                fill="url(#aqiGrad)"
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
