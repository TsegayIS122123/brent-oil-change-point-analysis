import React from 'react';
import { Grid, Card, CardContent, Typography } from '@mui/material';
import {
    AttachMoney,
    TrendingUp,
    Speed,
    Event,
    Bolt,
    TrackChanges
} from '@mui/icons-material';

const SummaryMetrics = ({ summary, changePoint }) => {
    const metrics = [
        {
            title: 'Current Price',
            value: `$${summary.latest_price || '0'}`,
            icon: <AttachMoney fontSize="small" />,
            color: '#1a237e'
        },
        {
            title: 'Annual Return',
            value: `${summary.annualized_return_pct || '0'}%`,
            icon: <TrendingUp fontSize="small" />,
            color: summary.annualized_return_pct > 0 ? '#4caf50' : '#f44336'
        },
        {
            title: 'Volatility',
            value: `${((summary.volatility || 0) * 100).toFixed(2)}%`,
            icon: <Speed fontSize="small" />,
            color: '#ff9800'
        },
        {
            title: 'Events Tracked',
            value: summary.total_events || '0',
            icon: <Event fontSize="small" />,
            color: '#9c27b0'
        },
        {
            title: 'Change Point',
            value: changePoint?.change_point_date || 'N/A',
            icon: <Bolt fontSize="small" />,
            color: '#ff9800'
        },
        {
            title: 'Price Impact',
            value: `${summary.price_impact_pct || '0'}%`,
            icon: <TrackChanges fontSize="small" />,
            color: summary.price_impact_pct > 0 ? '#4caf50' : '#f44336'
        }
    ];

    return (
        <Grid container spacing={2}>
            {metrics.map((metric, index) => (
                <Grid item xs={6} sm={4} md={2} key={index}>
                    <Card sx={{
                        height: '100%',
                        textAlign: 'center',
                        borderTop: `4px solid ${metric.color}`,
                        transition: 'transform 0.2s',
                        '&:hover': {
                            transform: 'translateY(-4px)'
                        }
                    }}>
                        <CardContent sx={{ p: 2 }}>
                            <Typography variant="h6" sx={{ color: metric.color, mb: 1 }}>
                                {metric.icon} {metric.value}
                            </Typography>
                            <Typography variant="caption" color="textSecondary">
                                {metric.title}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
            ))}
        </Grid>
    );
};

export default SummaryMetrics;