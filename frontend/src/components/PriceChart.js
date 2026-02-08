import React from 'react';
import {
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, Area, AreaChart, Line
} from 'recharts';

const PriceChart = ({ data, events, changePoint }) => {
  // Add event markers to chart data
  const chartData = data.map(item => {
    const event = events?.find(e => e.event_date === item.Date);
    return {
      ...item,
      eventPrice: event ? item.Price : null,
      eventName: event ? event.event_name : null
    };
  });

  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="Date"
          tickFormatter={(date) => {
            const d = new Date(date);
            return `${d.getMonth() + 1}/${d.getFullYear().toString().slice(-2)}`;
          }}
        />
        <YAxis />
        <Tooltip
          formatter={(value, name) => {
            if (name === 'Price') return [`$${parseFloat(value).toFixed(2)}`, 'Price'];
            if (name === 'eventPrice') return [`$${parseFloat(value).toFixed(2)}`, 'Event'];
            return [value, name];
          }}
          labelFormatter={(label) => new Date(label).toLocaleDateString()}
        />
        <Legend />
        <Area
          type="monotone"
          dataKey="Price"
          stroke="#1a237e"
          fill="#1a237e"
          fillOpacity={0.3}
          strokeWidth={2}
          name="Brent Price"
        />
        {/* Event markers */}
        {events?.map((event, index) => {
          const eventDataPoint = chartData.find(d => d.eventName === event.event_name);
          return eventDataPoint ? (
            <Line
              key={index}
              type="monotone"
              dataKey="eventPrice"
              stroke="#ff4444"
              strokeWidth={2}
              dot={{ r: 6, fill: '#ff4444' }}
              name="Events"
              data={[eventDataPoint]}
              hide
            />
          ) : null;
        })}
      </AreaChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;