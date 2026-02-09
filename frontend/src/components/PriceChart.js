import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Typography, Box } from '@mui/material';

const PriceChart = ({ data, events, changePoint }) => {
  // Format data for Recharts
  const chartData = React.useMemo(() => {
    if (!data || data.length === 0) {
      console.log('📊 No data for chart');
      return [];
    }

    console.log('📊 Chart data sample:', data.slice(0, 3));

    return data.map(item => ({
      date: new Date(item.Date).getTime(),
      Date: item.Date,
      Price: item.Price || 0,
      // Add event markers
      hasEvent: events?.some(e => e.event_date === item.Date) || false,
      eventName: events?.find(e => e.event_date === item.Date)?.event_name || null
    }));
  }, [data, events]);

  if (chartData.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height={400}>
        <Typography variant="body1" color="textSecondary">
          No price data available for the selected period
        </Typography>
      </Box>
    );
  }

  const formatXAxis = (tickItem) => {
    const date = new Date(tickItem);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
  };

  const formatTooltip = (value, name, props) => {
    if (name === 'Price') {
      return [`$${value.toFixed(2)}`, 'Brent Oil Price'];
    }
    return [value, name];
  };

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        data={chartData}
        margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis
          dataKey="date"
          tickFormatter={formatXAxis}
          type="number"
          domain={['dataMin', 'dataMax']}
          scale="time"
        />
        <YAxis
          label={{ value: 'Price (USD)', angle: -90, position: 'insideLeft' }}
          domain={['auto', 'auto']}
          tickFormatter={(value) => `$${value.toFixed(0)}`}
        />
        <Tooltip
          labelFormatter={(label) => {
            const date = new Date(label);
            return date.toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'short',
              day: 'numeric'
            });
          }}
          formatter={formatTooltip}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="Price"
          stroke="#1976d2"
          strokeWidth={2}
          dot={false}
          name="Brent Oil Price"
          activeDot={{ r: 6 }}
        />

        {/* Add change point reference line if available */}
        {changePoint && changePoint.change_point_date && (
          <ReferenceLine
            x={new Date(changePoint.change_point_date).getTime()}
            stroke="#ff6b6b"
            strokeWidth={2}
            strokeDasharray="3 3"
            label={{
              value: 'Change Point',
              position: 'top',
              fill: '#ff6b6b',
              fontSize: 12
            }}
          />
        )}
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;