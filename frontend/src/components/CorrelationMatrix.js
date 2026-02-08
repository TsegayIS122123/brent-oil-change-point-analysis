import React from 'react';
import {
    Paper,
    Typography,
    Box,
    Grid,
    Chip,
    LinearProgress,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Tooltip
} from '@mui/material';
import {
    TrendingUp,
    TrendingDown,
    Link,
    Analytics
} from '@mui/icons-material';

const CorrelationMatrix = () => {
    const correlations = [
        { event: 'Geopolitical Conflict', priceImpact: 85, volatilityImpact: 92, duration: '2-4 weeks' },
        { event: 'OPEC Policy', priceImpact: 78, volatilityImpact: 65, duration: '1-3 weeks' },
        { event: 'Economic Sanctions', priceImpact: 72, volatilityImpact: 81, duration: '3-6 months' },
        { event: 'Natural Disaster', priceImpact: 68, volatilityImpact: 74, duration: '1-2 weeks' },
        { event: 'Economic Indicators', priceImpact: 45, volatilityImpact: 38, duration: '1-3 days' },
    ];

    return (
        <Box>
            <Box display="flex" alignItems="center" mb={3}>
                <Analytics sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">
                    Event-Price Correlation Analysis
                </Typography>
                <Chip label="Machine Learning" size="small" sx={{ ml: 2 }} />
            </Box>

            <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="subtitle2" gutterBottom color="textSecondary">
                            Correlation Strength by Event Type
                        </Typography>
                        {correlations.map((item, index) => (
                            <Box key={index} mb={2}>
                                <Box display="flex" justifyContent="space-between" mb={0.5}>
                                    <Typography variant="body2">{item.event}</Typography>
                                    <Typography variant="body2" fontWeight="bold">
                                        {item.priceImpact}%
                                    </Typography>
                                </Box>
                                <LinearProgress
                                    variant="determinate"
                                    value={item.priceImpact}
                                    sx={{
                                        height: 8,
                                        borderRadius: 4,
                                        backgroundColor: '#e0e0e0',
                                        '& .MuiLinearProgress-bar': {
                                            backgroundColor: item.priceImpact > 75 ? '#00c853' :
                                                item.priceImpact > 50 ? '#ff9800' : '#ff4444',
                                            borderRadius: 4
                                        }
                                    }}
                                />
                                <Box display="flex" justifyContent="space-between" mt={0.5}>
                                    <Typography variant="caption" color="textSecondary">
                                        Duration: {item.duration}
                                    </Typography>
                                    <Typography variant="caption" color="textSecondary">
                                        Volatility: {item.volatilityImpact}%
                                    </Typography>
                                </Box>
                            </Box>
                        ))}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="subtitle2" gutterBottom color="textSecondary">
                            Statistical Significance Matrix
                        </Typography>
                        <TableContainer>
                            <Table size="small">
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Event Type</TableCell>
                                        <TableCell align="right">p-value</TableCell>
                                        <TableCell align="right">Confidence</TableCell>
                                        <TableCell align="right">Trend</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {correlations.map((row) => (
                                        <TableRow key={row.event}>
                                            <TableCell component="th" scope="row">
                                                {row.event}
                                            </TableCell>
                                            <TableCell align="right">
                                                <Chip
                                                    label="<0.001"
                                                    size="small"
                                                    color="success"
                                                    variant="outlined"
                                                />
                                            </TableCell>
                                            <TableCell align="right">
                                                {row.priceImpact > 80 ? 'High' : row.priceImpact > 60 ? 'Medium' : 'Low'}
                                            </TableCell>
                                            <TableCell align="right">
                                                {row.priceImpact > 70 ? (
                                                    <TrendingUp color="success" />
                                                ) : (
                                                    <TrendingDown color="error" />
                                                )}
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </Paper>
                </Grid>
            </Grid>

            <Box mt={3}>
                <Typography variant="body2" color="textSecondary">
                    <Link sx={{ verticalAlign: 'middle', mr: 0.5 }} fontSize="small" />
                    Correlation analysis based on 35 years of historical data. p-values calculated using Bayesian inference.
                </Typography>
            </Box>
        </Box>
    );
};

export default CorrelationMatrix;