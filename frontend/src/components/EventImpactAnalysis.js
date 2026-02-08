import React from 'react';
import {
    Grid,
    Card,
    CardContent,
    Typography,
    Box,
    Chip,
    Alert,
    LinearProgress
} from '@mui/material';
import {
    CalendarToday,
    Analytics,
    TrendingUp,
    Schedule
} from '@mui/icons-material';

const EventImpactAnalysis = ({ event, impact }) => {
    if (!event) return null;

    return (
        <Box>
            <Box display="flex" alignItems="center" mb={3}>
                <Analytics sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">
                    Event Impact Analysis
                </Typography>
            </Box>

            <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                <CalendarToday sx={{ verticalAlign: 'middle', mr: 1 }} />
                                Event Details
                            </Typography>
                            <Typography variant="body1" gutterBottom>
                                {event.event_name}
                            </Typography>
                            <Box display="flex" justifyContent="space-between" mt={1}>
                                <Typography variant="caption" color="textSecondary">
                                    Date: {event.event_date}
                                </Typography>
                                <Chip
                                    label={event.severity}
                                    size="small"
                                    color={
                                        event.severity === 'Very High' ? 'error' :
                                            event.severity === 'High' ? 'warning' :
                                                event.severity === 'Medium' ? 'info' : 'success'
                                    }
                                />
                            </Box>
                            <Typography variant="caption" color="textSecondary" display="block" mt={1}>
                                Type: {event.event_type}
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
                            {impact ? (
                                <>
                                    <Typography variant="h4" color={impact.price_impact?.percentage_change > 0 ? 'success.main' : 'error.main'}>
                                        {impact.price_impact?.percentage_change > 0 ? '+' : ''}
                                        {impact.price_impact?.percentage_change?.toFixed(1) || '0'}%
                                    </Typography>
                                    <Typography variant="caption" color="textSecondary">
                                        ${impact.price_impact?.before_event || '0'} → ${impact.price_impact?.after_event || '0'}
                                    </Typography>
                                    <Box mt={2}>
                                        <LinearProgress
                                            variant="determinate"
                                            value={Math.min(Math.abs(impact.price_impact?.percentage_change || 0), 100)}
                                            sx={{
                                                height: 8,
                                                borderRadius: 4,
                                                '& .MuiLinearProgress-bar': {
                                                    backgroundColor: impact.price_impact?.percentage_change > 0 ? '#4caf50' : '#f44336',
                                                    borderRadius: 4
                                                }
                                            }}
                                        />
                                    </Box>
                                </>
                            ) : (
                                <Alert severity="info" sx={{ mt: 1 }}>
                                    Loading impact analysis...
                                </Alert>
                            )}
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                <Schedule sx={{ verticalAlign: 'middle', mr: 1 }} />
                                Analysis Period
                            </Typography>
                            {impact ? (
                                <>
                                    <Typography variant="body2" gutterBottom>
                                        {impact.impact_window?.start_date || 'N/A'}
                                    </Typography>
                                    <Typography variant="body2" align="center" sx={{ fontWeight: 'bold' }}>
                                        to
                                    </Typography>
                                    <Typography variant="body2">
                                        {impact.impact_window?.end_date || 'N/A'}
                                    </Typography>
                                    <Box mt={2}>
                                        <Typography variant="caption" color="textSecondary">
                                            Window: ±{impact.impact_window?.days_before || 30} days
                                        </Typography>
                                    </Box>
                                </>
                            ) : (
                                <Typography variant="body2" color="textSecondary">
                                    Impact analysis period will be shown here
                                </Typography>
                            )}
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
};

export default EventImpactAnalysis;