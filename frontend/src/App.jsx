/**
 * CityPulse AI — Main Application
 * Assembles all dashboard components with real-time WebSocket data.
 * Supports dynamic city switching.
 */
import { useWebSocket } from './hooks/useWebSocket';
import Navbar from './components/Navbar';
import KPICards from './components/KPICards';
import TrafficChart from './components/TrafficChart';
import AQIChart from './components/AQIChart';
import EnergyChart from './components/EnergyChart';
import AlertsPanel from './components/AlertsPanel';
import CityMap from './components/CityMap';
import ZoneTable from './components/ZoneTable';

function App() {
  const {
    isConnected,
    zoneData,
    alerts,
    historyData,
    activeCity,
    cities,
    switchCity,
  } = useWebSocket();

  return (
    <div className="app">
      <Navbar
        isConnected={isConnected}
        activeCity={activeCity}
        cities={cities}
        onCityChange={switchCity}
      />

      <main className="main-content">
        {/* KPI Summary Cards */}
        <KPICards zoneData={zoneData} alertCount={alerts.length} />

        {/* Charts + Alerts Grid */}
        <div className="dashboard-grid">
          <TrafficChart historyData={historyData} />
          <AQIChart historyData={historyData} />
          <EnergyChart historyData={historyData} />
          <AlertsPanel alerts={alerts} />
        </div>

        {/* City Map */}
        <CityMap zoneData={zoneData} activeCity={activeCity} />

        {/* Zone Detail Table */}
        <ZoneTable zoneData={zoneData} />
      </main>
    </div>
  );
}

export default App;
