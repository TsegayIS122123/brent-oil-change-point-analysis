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
  ExportPanel,
  EventTypePieChart,
  VolatilityChart
} from './components';

// Configure axios to handle errors better
axios.defaults.timeout = 10000; // 10 second timeout
const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  // State management
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState(0);
  const [showExport, setShowExport] = useState(false);
  const [error, setError] = useState(null);

  // Raw data states
  const [rawPriceData, setRawPriceData] = useState([]);
  const [rawEvents, setRawEvents] = useState([]);
  const [changePoint, setChangePoint] = useState(null);
  const [summary, setSummary] = useState({});
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

  // SIMPLE AND ROBUST fetchData function
  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    console.log('🔄 Starting data fetch...');

    try {
      // Test connection first
      console.log('🔗 Testing connection to:', `${API_BASE_URL}/`);
      const test = await axios.get(`${API_BASE_URL}/`, { timeout: 5000 });
      console.log('✅ Backend test successful:', test.data);

      // Fetch data - handle each individually
      const requests = [
        { name: 'prices', url: `${API_BASE_URL}/prices` },
        { name: 'events', url: `${API_BASE_URL}/events` },
        { name: 'change-point', url: `${API_BASE_URL}/change-point` },
        { name: 'summary', url: `${API_BASE_URL}/summary` }
      ];

      const results = {};

      for (const req of requests) {
        try {
          console.log(`📥 Fetching ${req.name}...`);
          const response = await axios.get(req.url, { timeout: 10000 });
          console.log(`✅ ${req.name} response:`, response.status, response.data ? 'has data' : 'no data');

          // Handle the response based on API structure
          if (response.data) {
            if (req.name === 'prices') {
              setRawPriceData(response.data.data || response.data || []);
              console.log(`💰 Loaded ${(response.data.data || response.data || []).length} price records`);
            } else if (req.name === 'events') {
              setRawEvents(response.data.data || response.data || []);
              console.log(`🎯 Loaded ${(response.data.data || response.data || []).length} events`);
            } else if (req.name === 'change-point') {
              setChangePoint(response.data.data || response.data || {});
            } else if (req.name === 'summary') {
              setSummary(response.data.data || response.data || {});
            }
          }
        } catch (reqError) {
          console.warn(`⚠️ ${req.name} fetch failed:`, reqError.message);
          // Continue with other requests even if one fails
        }
      }

      console.log('🎉 Data fetch completed');

    } catch (error) {
      console.error('❌ Fetch error details:', {
        message: error.message,
        code: error.code,
        response: error.response?.data,
        status: error.response?.status,
        url: error.config?.url
      });

      if (error.code === 'ECONNABORTED') {
        setError('Request timeout. Backend might be slow to respond.');
      } else if (error.response) {
        setError(`Backend error ${error.response.status}: ${JSON.stringify(error.response.data)}`);
      } else if (error.request) {
        setError('No response from backend. Is Flask running on port 5000?');
      } else {
        setError(`Connection error: ${error.message}`);
      }
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
      const response = await axios.get(`${API_BASE_URL}/event-impact/${event.id}`);
      console.log('📊 Event impact response:', response.data);

      if (response.data && response.data.success !== false) {
        setEventImpact(response.data.data || response.data);
      }
    } catch (error) {
      console.warn('⚠️ Event impact fetch failed:', error.message);
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
            <br />2. Check if accessible: <a href="http://localhost:5000/api/prices" target="_blank" rel="noreferrer">http://localhost:5000/api/prices</a>
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
          Connecting to backend API...
        </Typography>
      </Box>
    );
  }

  // Check if we have data
  const hasData = rawPriceData.length > 0 || rawEvents.length > 0;

  if (!hasData) {
    return (
      <Box sx={{ bgcolor: '#f5f7fa', minHeight: '100vh', p: 3 }}>
        <DashboardHeader onExport={() => setShowExport(true)} onRefresh={fetchData} activeTab={activeTab} />
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
              <br />1. Open <a href="http://localhost:5000/api/prices" target="_blank" rel="noreferrer">http://localhost:5000/api/prices</a> in browser
              <br />2. Check browser console (F12) for errors
              <br />3. Check if CSV files exist in data/ folder
            </Typography>
          </Box>
        </Container>
      </Box>
    );
  }

  return (
    <Box sx={{ bgcolor: '#f5f7fa', minHeight: '100vh' }}>
      <DashboardHeader onExport={() => setShowExport(true)} onRefresh={fetchData} activeTab={activeTab} />

      <Container maxWidth="xl" sx={{ py: 3 }}>
        {/* Success Alert */}
        <Alert severity="success" sx={{ mb: 3, borderRadius: 2 }} icon={<Timeline />}>
          <Typography variant="subtitle2">
            ✅ Real Data Loaded: {rawPriceData.length} prices • {rawEvents.length} events
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
                  <PriceChart data={filteredData.prices} events={filteredData.events} changePoint={changePoint} />
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
                <EventsTimeline events={filteredData.events} onEventSelect={handleEventSelect} selectedEvent={selectedEvent} />
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
                <VolatilityChart priceData={filteredData.prices} />
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
                <EventsTimeline events={filteredData.events} onEventSelect={handleEventSelect} selectedEvent={selectedEvent} />
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
            Brent Oil Intelligence Dashboard • Real Data • {new Date().toLocaleDateString()}
          </Typography>
        </Box>
      </Container>

      <ExportPanel open={showExport} onClose={() => setShowExport(false)} />
    </Box>
  );
}

export default App;