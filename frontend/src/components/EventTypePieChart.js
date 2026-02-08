import React from 'react';
import {
    Paper,
    Typography,
    Box,
    Grid,
    Card,
    CardContent
} from '@mui/material';
import {
    PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend
} from 'recharts';
import {
    CrisisAlert,
    Policy,
    TrendingDown,
    Gavel,
    Cloud
} from '@mui/icons-material';

const EventTypePieChart = ({ events }) => {
    // Calculate event type distribution
    const eventTypes = {
        'Geopolitical': events.filter(e => e.event_type.includes('Geopolitical')).length,
        'OPEC Policy': events.filter(e => e.event_type.includes('OPEC')).length,
        'Economic': events.filter(e => e.event_type.includes('Economic')).length,
        'Sanctions': events.filter(e => e.event_type.includes('Sanctions')).length,
        'Natural Disaster': events.filter(e => e.event_type.includes('Disaster')).length
    };

    const pieData = Object.entries(eventTypes)
        .filter(([_, value]) => value > 0)
        .map(([name, value]) => ({ name, value }));

    const COLORS = ['#ff4444', '#33b5e5', '#00c851', '#ffbb33', '#aa66cc'];

    const getIcon = (eventType) => {
        switch (eventType) {
            case 'Geopolitical': return <CrisisAlert sx={{ color: '#ff4444' }} />;
            case 'OPEC Policy': return <Policy sx={{ color: '#33b5e5' }} />;
            case 'Economic': return <TrendingDown sx={{ color: '#00c851' }} />;
            case 'Sanctions': return <Gavel sx={{ color: '#ffbb33' }} />;
            case 'Natural Disaster': return <Cloud sx={{ color: '#aa66cc' }} />;
            default: return null;
        }
    };

    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom color="primary">
                    Event Type Distribution
                </Typography>

                <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                        <Box sx={{ height: 250 }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={pieData}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                                        outerRadius={80}
                                        fill="#8884d8"
                                        dataKey="value"
                                    >
                                        {pieData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip formatter={(value) => [`${value} events`, 'Count']} />
                                    <Legend />
                                </PieChart>
                            </ResponsiveContainer>
                        </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                        <Box sx={{ height: 250, overflow: 'auto' }}>
                            {pieData.map((item, index) => (
                                <Box
                                    key={item.name}
                                    display="flex"
                                    alignItems="center"
                                    justifyContent="space-between"
                                    sx={{
                                        mb: 1.5,
                                        p: 1.5,
                                        borderRadius: 1,
                                        bgcolor: 'background.default'
                                    }}
                                >
                                    <Box display="flex" alignItems="center">
                                        {getIcon(item.name)}
                                        <Typography variant="body2" sx={{ ml: 1.5, fontWeight: 'medium' }}>
                                            {item.name}
                                        </Typography>
                                    </Box>
                                    <Box display="flex" alignItems="center">
                                        <Typography variant="h6" sx={{ color: COLORS[index], mr: 1 }}>
                                            {item.value}
                                        </Typography>
                                        <Typography variant="caption" color="textSecondary">
                                            events
                                        </Typography>
                                    </Box>
                                </Box>
                            ))}

                            {/* Total events */}
                            <Box
                                display="flex"
                                alignItems="center"
                                justifyContent="space-between"
                                sx={{
                                    mt: 2,
                                    pt: 2,
                                    borderTop: 1,
                                    borderColor: 'divider'
                                }}
                            >
                                <Typography variant="subtitle2" color="primary">
                                    Total Events
                                </Typography>
                                <Typography variant="h5" color="primary">
                                    {events.length}
                                </Typography>
                            </Box>
                        </Box>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );
};

export default EventTypePieChart;