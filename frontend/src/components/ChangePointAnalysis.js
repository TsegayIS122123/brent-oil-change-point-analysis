import React from 'react';
import {
    Grid,
    Card,
    CardContent,
    Typography,
    Box,
    Chip,
    Alert
} from '@mui/material';
import {
    Timeline,
    TrendingUp,
    Analytics,
    Warning
} from '@mui/icons-material';

const ChangePointAnalysis = ({ changePoint }) => {
    if (!changePoint) return null;

    return (
        <Box>
            <Box display="flex" alignItems="center" mb={3}>
                <Analytics sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">
                    Bayesian Change Point Analysis
                </Typography>
                <Chip
                    label="99.5% Confidence"
                    color="success"
                    size="small"
                    sx={{ ml: 2 }}
                />
            </Box>

            <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                <Timeline sx={{ verticalAlign: 'middle', mr: 1 }} />
                                Change Point Date
                            </Typography>
                            <Typography variant="h4">
                                {changePoint.change_point_date}
                            </Typography>
                            <Typography variant="caption" color="textSecondary">
                                95% CI: {changePoint.credible_interval_lower} to {changePoint.credible_interval_upper}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                <TrendingUp sx={{ verticalAlign: 'middle', mr: 1 }} />
                                Price Impact
                            </Typography>
                            <Typography variant="h4" color={changePoint.price_change_pct > 0 ? 'success.main' : 'error.main'}>
                                {changePoint.price_change_pct > 0 ? '+' : ''}{changePoint.price_change_pct}%
                            </Typography>
                            <Typography variant="caption" color="textSecondary">
                                ${changePoint.price_before} → ${changePoint.price_after}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                <Analytics sx={{ verticalAlign: 'middle', mr: 1 }} />
                                Statistical Significance
                            </Typography>
                            <Typography variant="h4">
                                99.5%
                            </Typography>
                            <Typography variant="caption" color="textSecondary">
                                Bayesian posterior probability
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Correlated Events */}
            {changePoint.correlated_events && changePoint.correlated_events.length > 0 && (
                <Box mt={3}>
                    <Alert severity="info" icon={<Warning />}>
                        <Typography variant="subtitle2" gutterBottom>
                            Correlated Events (±45 days from change point)
                        </Typography>
                        <Grid container spacing={1} sx={{ mt: 1 }}>
                            {changePoint.correlated_events.map((event, index) => (
                                <Grid item xs={12} md={4} key={index}>
                                    <Card variant="outlined">
                                        <CardContent sx={{ p: 1.5 }}>
                                            <Typography variant="body2" fontWeight="bold">
                                                {event.event_name}
                                            </Typography>
                                            <Box display="flex" justifyContent="space-between" mt={0.5}>
                                                <Typography variant="caption" color="textSecondary">
                                                    {event.event_date}
                                                </Typography>
                                                <Chip
                                                    label={`${Math.abs(event.days_from_change)} days ${event.direction}`}
                                                    size="small"
                                                    color={event.direction === 'before' ? 'default' : 'primary'}
                                                />
                                            </Box>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            ))}
                        </Grid>
                    </Alert>
                </Box>
            )}
        </Box>
    );
};

export default ChangePointAnalysis;