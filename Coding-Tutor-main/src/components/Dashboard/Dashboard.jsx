import React from 'react';
import ErrorStats from './ErrorStats';
import './Dashboard.css';

const Dashboard = ({ stats }) => {
  const successRate = stats.totalRuns > 0
    ? ((stats.successCount / stats.totalRuns) * 100).toFixed(1)
    : 0;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Runs</div>
          <div className="stat-value">{stats.totalRuns}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Success Rate</div>
          <div className="stat-value">{successRate}%</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Errors</div>
          <div className="stat-value">{stats.errorCount}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Hints Requested</div>
          <div className="stat-value">{stats.hintsRequested}</div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-section">
          <h2>Error Statistics</h2>
          <ErrorStats stats={stats} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;


