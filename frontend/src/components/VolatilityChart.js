import React from 'react';
import {
    Paper,
    Typography,
    Box,
    Card,
    CardContent,
    Grid
} from '@mui/material';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    BarChart, Bar, Legend
} from 'recharts';
import { TrendingUp, Speed, Warning } from '@mui/icons-material';

const VolatilityChart = ({ priceData }) => {
    // Calculate rolling volatility (simplified)
    const calculateVolatility = (prices, window = 20) => {
        const volatilityData = [];

        for (let i = window; i < prices.length; i++) {
            const windowPrices = prices.slice(i - window, i);
            const returns = windowPrices.slice(1).map((price, idx) =>
                Math.log(price.Price / windowPrices[idx].Price)
            );

            const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
            const variance = returns.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / returns.length;
            const volatility = Math.sqrt(variance) * Math.sqrt(252); // Annualized

            volatilityData.push({
                Date: prices[i].Date,
                Volatility: (volatility * 100).toFixed(2),
                Price: prices[i].Price
            });
        }

        return volatilityData.slice(-100); // Last 100 points
    };

    const volatilityData = priceData.length > 20 ? calculateVolatility(priceData) : [];

    // Volatility statistics
    const volatilityStats = {
        current: volatilityData.length > 0 ? parseFloat(volatilityData[volatilityData.length - 1].Volatility) : 0,
        average: volatilityData.length > 0
            ? (volatilityData.reduce((sum, item) => sum + parseFloat(item.Volatility), 0) / volatilityData.length).toFixed(2)
            : 0,
        max: volatilityData.length > 0
            ? Math.max(...volatilityData.map(item => parseFloat(item.Volatility))).toFixed(2)
            : 0,
        min: volatilityData.length > 0
            ? Math.min(...volatilityData.map(item => parseFloat(item.Volatility))).toFixed(2)
            : 0
    };

    return (
        <Box>
            <Box display="flex" alignItems="center" mb={3}>
                <Speed sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">
                    Volatility Analysis
                </Typography>
                <Warning
                    color={volatilityStats.current > 40 ? "error" : volatilityStats.current > 30 ? "warning" : "success"}
                    sx={{ ml: 2 }}
                />
            </Box>

            <Grid container spacing={3}>
                {/* Volatility Statistics */}
                <Grid item xs={12}>
                    <Grid container spacing={2}>
                        {[
                            {
                                title: 'Current Volatility', value: `${volatilityStats.current}%`, icon: <Speed />,
                                color: volatilityStats.current > 40 ? 'error.main' : volatilityStats.current > 30 ? 'warning.main' : 'success.main'
                            },
                            { title: 'Average Volatility', value: `${volatilityStats.average}%`, icon: <TrendingUp /> },
                            { title: 'Maximum Volatility', value: `${volatilityStats.max}%`, icon: <Warning />, color: 'error.main' },
                            { title: 'Minimum Volatility', value: `${volatilityStats.min}%`, icon: <TrendingUp />, color: 'success.main' }
                        ].map((stat, index) => (
                            <Grid item xs={6} md={3} key={index}>
                                <Card>
                                    <CardContent sx={{ textAlign: 'center', p: 2 }}>
                                        <Typography variant="h6" sx={{ color: stat.color || 'primary.main', mb: 1 }}>
                                            {stat.icon} {stat.value}
                                        </Typography>
                                        <Typography variant="caption" color="textSecondary">
                                            {stat.title}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                </Grid>

                {/* Volatility Chart */}
                <Grid item xs={12} md={8}>
                    <Paper sx={{ p: 2, borderRadius: 2 }}>
                        <Typography variant="subtitle2" gutterBottom color="textSecondary">
                            20-Day Rolling Volatility (Annualized)
                        </Typography>
                        <Box sx={{ height: 300 }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={volatilityData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis
                                        dataKey="Date"
                                        tickFormatter={(date) => {
                                            const d = new Date(date);
                                            return `${d.getMonth() + 1}/${d.getDate()}`;
                                        }}
                                    />
                                    <YAxis label={{ value: 'Volatility %', angle: -90, position: 'insideLeft' }} />
                                    <Tooltip
                                        formatter={(value) => [`${value}%`, 'Volatility']}
                                        labelFormatter={(label) => new Date(label).toLocaleDateString()}
                                    />
                                    <Area
                                        type="monotone"
                                        dataKey="Volatility"
                                        stroke="#ff9800"
                                        fill="#ff9800"
                                        fillOpacity={0.3}
                                        strokeWidth={2}
                                    />
                                </AreaChart>
                            </ResponsiveContainer>
                        </Box>
                    </Paper>
                </Grid>

                {/* Price vs Volatility */}
                <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 2, borderRadius: 2 }}>
                        <Typography variant="subtitle2" gutterBottom color="textSecondary">
                            Price vs Volatility Relationship
                        </Typography>
                        <Box sx={{ height: 300 }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={volatilityData.slice(-10)}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis
                                        dataKey="Date"
                                        tickFormatter={(date) => {
                                            const d = new Date(date);
                                            return `${d.getMonth() + 1}/${d.getDate()}`;
                                        }}
                                    />
                                    <YAxis />
                                    <Tooltip
                                        formatter={(value, name) => {
                                            if (name === 'Price') return [`$${value}`, 'Price'];
                                            if (name === 'Volatility') return [`${value}%`, 'Volatility'];
                                            return [value, name];
                                        }}
                                    />
                                    <Legend />
                                    <Bar dataKey="Price" fill="#1a237e" name="Price ($)" />
                                    <Bar dataKey="Volatility" fill="#ff9800" name="Volatility (%)" />
                                </BarChart>
                            </ResponsiveContainer>
                        </Box>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default VolatilityChart;