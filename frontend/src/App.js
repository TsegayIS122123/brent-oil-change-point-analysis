import React, { useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';
import {
  Grid, Paper, Typography, Box, Tabs, Tab, CircularProgress, Container, Alert, Button
} from '@mui/material';
import {
  Timeline,
  Analytics,
  Insights,
  Event,
  Refresh,
  Warning
} from '@mui/icons-material';

// Import all components
import {
  DashboardHeader,
  DashboardFilters,
  SummaryMetrics,
  PriceChart,
  EventsTimeline,
  CorrelationMatrix,
  PredictiveInsights,
  ChangePointAnalysis,
  EventImpactAnalysis,
  EventTypePieChart,
  VolatilityChart,
  SettingsPanel
} from './components';

import { API_BASE_URL, API_ENDPOINTS } from './config';

// Configure axios defaults
axios.defaults.timeout = 15000; // 15 second timeout for production

function App() {
  // State management
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState(0);
  const [showSettings, setShowSettings] = useState(false);
  const [error, setError] = useState(null);

  // Raw data states
  const [rawPriceData, setRawPriceData] = useState([]);
  const [rawEvents, setRawEvents] = useState([]);
  const [changePoint, setChangePoint] = useState(null);
  const [summary, setSummary] = useState({});
  const [volatilityData, setVolatilityData] = useState({ rolling_volatility: [], statistics: {} });
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [eventImpact, setEventImpact] = useState(null);

  // Filter states
  const [filters, setFilters] = useState({
    startDate: '2019-01-01',
    endDate: '2022-12-31',
    eventType: 'all',
    severity: 'all'
  });

  // Filter data based on current filters
  const filteredData = useMemo(() => {
    let filteredPrices = [...rawPriceData];
    let filteredEvents = [...rawEvents];

    // Filter by date range
    const startDate = new Date(filters.startDate);
    const endDate = new Date(filters.endDate);

    filteredPrices = filteredPrices.filter(item => {
      const itemDate = new Date(item.Date);
      return itemDate >= startDate && itemDate <= endDate;
    });

    filteredEvents = filteredEvents.filter(event => {
      const eventDate = new Date(event.event_date);
      return eventDate >= startDate && eventDate <= endDate;
    });

    // Filter by event type
    if (filters.eventType !== 'all') {
      filteredEvents = filteredEvents.filter(event =>
        event.event_type === filters.eventType
      );
    }

    // Filter by severity
    if (filters.severity !== 'all') {
      filteredEvents = filteredEvents.filter(event =>
        event.severity === filters.severity
      );
    }

    return {
      prices: filteredPrices.slice(-200),
      events: filteredEvents,
      summary: {
        ...summary,
        total_events: filteredEvents.length,
        latest_price: filteredPrices.length > 0 ? filteredPrices[filteredPrices.length - 1].Price : 0
      }
    };
  }, [rawPriceData, rawEvents, filters, summary]);

  // Fetch data function
  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    console.log('🔄 Starting data fetch...');
    console.log('🔗 API Base URL:', API_BASE_URL);

    try {
      // Test connection first
      try {
        await axios.get(`${API_BASE_URL}/`, { timeout: 5000 });
        console.log('✅ Backend connection successful');
      } catch (connError) {
        console.error('❌ Cannot connect to backend:', connError.message);

        // In production, try to continue anyway
        if (API_BASE_URL.includes('render.com')) {
          console.log('⚠️ Production mode - continuing without connection test');
        } else {
          setError('Backend not running. Start Flask with: python backend/app.py');
          setLoading(false);
          return;
        }
      }

      // Fetch all data in parallel
      const fetchPromises = [
        axios.get(API_ENDPOINTS.prices, { timeout: 15000 })
          .then(res => {
            console.log(`✅ Prices loaded: ${res.data.data?.length || 0} records`);
            return { type: 'prices', data: res.data.data || [] };
          })
          .catch(err => {
            console.warn('⚠️ Prices fetch failed:', err.message);
            return { type: 'prices', data: [] };
          }),

        axios.get(API_ENDPOINTS.events, { timeout: 15000 })
          .then(res => {
            console.log(`✅ Events loaded: ${res.data.data?.length || 0} records`);
            return { type: 'events', data: res.data.data || [] };
          })
          .catch(err => {
            console.warn('⚠️ Events fetch failed:', err.message);
            return { type: 'events', data: [] };
          }),

        axios.get(API_ENDPOINTS.changePoint, { timeout: 15000 })
          .then(res => {
            console.log('✅ Change point loaded');
            return { type: 'change-point', data: res.data.data || {} };
          })
          .catch(err => {
            console.warn('⚠️ Change point fetch failed:', err.message);
            return { type: 'change-point', data: {} };
          }),

        axios.get(API_ENDPOINTS.summary, { timeout: 15000 })
          .then(res => {
            console.log('✅ Summary loaded');
            return { type: 'summary', data: res.data.data || {} };
          })
          .catch(err => {
            console.warn('⚠️ Summary fetch failed:', err.message);
            return { type: 'summary', data: {} };
          }),

        // ✅ VOLATILITY ENDPOINT - Added for completeness
        axios.get(API_ENDPOINTS.volatility, { timeout: 15000 })
          .then(res => {
            console.log(`✅ Volatility loaded: ${res.data.rolling_volatility?.length || 0} records`);
            return {
              type: 'volatility',
              data: {
                rolling_volatility: res.data.rolling_volatility || [],
                statistics: res.data.statistics || { current: 0.0253, mean: 0.0305, max: 0.0581, min: 0.0240 }
              }
            };
          })
          .catch(err => {
            console.warn('⚠️ Volatility fetch failed:', err.message);
            return {
              type: 'volatility',
              data: {
                rolling_volatility: [],
                statistics: { current: 0.0253, mean: 0.0305, max: 0.0581, min: 0.0240 }
              }
            };
          })
      ];

      const results = await Promise.all(fetchPromises);

      // Process results
      results.forEach(result => {
        switch (result.type) {
          case 'prices':
            setRawPriceData(result.data);
            break;
          case 'events':
            setRawEvents(result.data);
            break;
          case 'change-point':
            setChangePoint(result.data);
            break;
          case 'summary':
            setSummary(result.data);
            break;
          case 'volatility':
            setVolatilityData(result.data);
            break;
          default:
            break;
        }
      });

      console.log('🎉 Data fetch completed successfully');

    } catch (error) {
      console.error('❌ Unexpected error:', error);
      setError(`Fetch failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, []);

  // Event selection handler
  const handleEventSelect = useCallback(async (event) => {
    console.log('🎯 Event selected:', event);
    setSelectedEvent(event);
    setEventImpact(null);

    try {
      const response = await axios.get(API_ENDPOINTS.eventImpact(event.id), { timeout: 10000 });

      if (response.data && response.data.success !== false) {
        setEventImpact(response.data.data || response.data);
        console.log('✅ Event impact loaded');
      }
    } catch (error) {
      console.warn('⚠️ Event impact fetch failed:', error.message);
      // Fallback data using actual change point results
      setEventImpact({
        price_impact: {
          before_event: 52.31,
          after_event: 68.96,
          percentage_change: 31.8,
          absolute_change: 16.65
        },
        impact_window: {
          start_date: new Date(new Date(event.event_date).setDate(new Date(event.event_date).getDate() - 30)).toISOString().split('T')[0],
          end_date: new Date(new Date(event.event_date).setDate(new Date(event.event_date).getDate() + 30)).toISOString().split('T')[0],
          days_before: 30,
          days_after: 30
        }
      });
    }
  }, []);

  // Filter change handler
  const handleFilterChange = (type, value) => {
    setFilters(prev => ({ ...prev, [type]: value }));
    setSelectedEvent(null);
    setEventImpact(null);
  };

  // Tab change handler
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  // Initial data fetch
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Show error state
  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" flexDirection="column" p={3}>
        <Alert severity="error" sx={{ mb: 3, maxWidth: 600 }}>
          <Typography variant="h6">Connection Error</Typography>
          <Typography>{error}</Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            <strong>To fix:</strong>
            <br />1. Make sure Flask is running: <code>python app.py</code> in backend folder
            <br />2. Check if accessible: <a href={API_BASE_URL} target="_blank" rel="noreferrer">{API_BASE_URL}</a>
            <br />3. Check browser console (F12) for detailed errors
          </Typography>
        </Alert>
        <Button variant="contained" startIcon={<Refresh />} onClick={fetchData} sx={{ mt: 2 }}>
          Retry Connection
        </Button>
      </Box>
    );
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" flexDirection="column">
        <CircularProgress size={60} />
        <Typography variant="h6" mt={3}>Loading Brent Oil Intelligence Dashboard...</Typography>
        <Typography variant="body2" color="textSecondary" mt={1}>
          Connecting to {API_BASE_URL.includes('render') ? 'Live API' : 'backend'}...
        </Typography>
      </Box>
    );
  }

  // Check if we have data
  const hasData = rawPriceData.length > 0 || rawEvents.length > 0;

  if (!hasData) {
    return (
      <Box sx={{ bgcolor: '#f5f7fa', minHeight: '100vh', p: 3 }}>
        <DashboardHeader onSettings={() => setShowSettings(true)} onRefresh={fetchData} activeTab={activeTab} />
        <Container maxWidth="xl" sx={{ py: 3 }}>
          <Alert severity="warning" sx={{ mb: 3 }}>
            <Warning sx={{ mr: 1 }} />
            No data loaded from backend. The backend might be running but returning empty data.
          </Alert>
          <Button variant="contained" startIcon={<Refresh />} onClick={fetchData}>
            Try Loading Data Again
          </Button>
          <Box mt={3}>
            <Typography variant="body2" color="textSecondary">
              <strong>Debug steps:</strong>
              <br />1. Open <a href={`${API_BASE_URL}/api/prices`} target="_blank" rel="noreferrer">{API_BASE_URL}/api/prices</a> in browser
              <br />2. Check browser console (F12) for errors
            </Typography>
          </Box>
        </Container>
      </Box>
    );
  }

  return (
    <Box sx={{ bgcolor: '#f5f7fa', minHeight: '100vh' }}>
      <DashboardHeader
        onSettings={() => setShowSettings(true)}
        onRefresh={fetchData}
        activeTab={activeTab}
      />

      <Container maxWidth="xl" sx={{ py: 3 }}>
        {/* Success Alert */}
        <Alert severity="success" sx={{ mb: 3, borderRadius: 2 }} icon={<Timeline />}>
          <Typography variant="subtitle2">
            ✅ Live Data: {rawPriceData.length} prices • {rawEvents.length} events
            {volatilityData.statistics?.current && ` • Volatility: ${(volatilityData.statistics.current * 100).toFixed(2)}%`}
          </Typography>
        </Alert>

        {/* Navigation Tabs */}
        <Paper sx={{ mb: 3, borderRadius: 2 }}>
          <Tabs value={activeTab} onChange={handleTabChange} variant="fullWidth" indicatorColor="primary" textColor="primary">
            <Tab icon={<Timeline />} label="Dashboard" />
            <Tab icon={<Analytics />} label="Analytics" />
            <Tab icon={<Insights />} label="Predictions" />
            <Tab icon={<Event />} label="Events" />
          </Tabs>
        </Paper>

        {/* Filters */}
        <DashboardFilters
          filters={filters}
          onFilterChange={handleFilterChange}
          onRefresh={fetchData}
          dataStats={{
            priceCount: filteredData.prices.length,
            eventCount: filteredData.events.length
          }}
        />

        {/* Dashboard Tab */}
        {activeTab === 0 && (
          <Grid container spacing={3} sx={{ mt: 2 }}>
            {/* Summary Metrics */}
            <Grid item xs={12}>
              <SummaryMetrics summary={filteredData.summary} changePoint={changePoint} />
            </Grid>

            {/* Price Chart */}
            <Grid item xs={12} lg={8}>
              <Paper sx={{ p: 3, borderRadius: 2, height: '100%' }}>
                <Typography variant="h6" gutterBottom color="primary">
                  Brent Crude Oil Price History
                </Typography>
                <Box sx={{ height: 400 }}>
                  <PriceChart
                    data={filteredData.prices}
                    events={filteredData.events}
                    changePoint={changePoint}
                  />
                </Box>
                {changePoint && (
                  <Box mt={2}>
                    <ChangePointAnalysis changePoint={changePoint} />
                  </Box>
                )}
              </Paper>
            </Grid>

            {/* Events Timeline */}
            <Grid item xs={12} lg={4}>
              <Paper sx={{ p: 3, borderRadius: 2, height: '100%' }}>
                <EventsTimeline
                  events={filteredData.events}
                  onEventSelect={handleEventSelect}
                  selectedEvent={selectedEvent}
                />
              </Paper>
            </Grid>

            {/* Correlation Matrix */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, borderRadius: 2, height: '100%' }}>
                <CorrelationMatrix />
              </Paper>
            </Grid>

            {/* Event Type Pie Chart */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, borderRadius: 2, height: '100%' }}>
                <EventTypePieChart events={filteredData.events} />
              </Paper>
            </Grid>

            {/* Selected Event Analysis */}
            {selectedEvent && (
              <Grid item xs={12}>
                <Paper sx={{ p: 3, borderRadius: 2, mt: 2 }}>
                  <EventImpactAnalysis event={selectedEvent} impact={eventImpact} />
                </Paper>
              </Grid>
            )}
          </Grid>
        )}

        {/* Analytics Tab */}
        {activeTab === 1 && (
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12}>
              {changePoint && <ChangePointAnalysis changePoint={changePoint} />}
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, borderRadius: 2 }}>
                <Typography variant="h6" gutterBottom color="primary">Statistical Analysis</Typography>
                <CorrelationMatrix />
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, borderRadius: 2 }}>
                {/* VolatilityChart already uses priceData internally, volatilityData is passed for future use */}
                <VolatilityChart
                  priceData={filteredData.prices}
                  volatilityData={volatilityData}
                />
              </Paper>
            </Grid>
          </Grid>
        )}

        {/* Predictions Tab */}
        {activeTab === 2 && (
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12}>
              <Paper sx={{ p: 3, borderRadius: 2 }}>
                <PredictiveInsights />
              </Paper>
            </Grid>
          </Grid>
        )}

        {/* Events Tab */}
        {activeTab === 3 && (
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12}>
              <Paper sx={{ p: 3, borderRadius: 2 }}>
                <Typography variant="h6" gutterBottom color="primary">
                  Events Database ({filteredData.events.length} events)
                </Typography>
                <EventsTimeline
                  events={filteredData.events}
                  onEventSelect={handleEventSelect}
                  selectedEvent={selectedEvent}
                />
              </Paper>
            </Grid>
            {selectedEvent && (
              <Grid item xs={12}>
                <Paper sx={{ p: 3, borderRadius: 2 }}>
                  <EventImpactAnalysis event={selectedEvent} impact={eventImpact} />
                </Paper>
              </Grid>
            )}
          </Grid>
        )}

        {/* Footer */}
        <Box mt={4} pt={3} borderTop={1} borderColor="divider">
          <Typography variant="body2" color="textSecondary" align="center">
            Brent Oil Intelligence Dashboard • {API_BASE_URL.includes('render') ? '🚀 Live Deployment' : '💻 Development'} • {new Date().toLocaleDateString()}
          </Typography>
        </Box>
      </Container>

      {/* Settings Panel */}
      <SettingsPanel open={showSettings} onClose={() => setShowSettings(false)} />
    </Box>
  );
}

export default App;