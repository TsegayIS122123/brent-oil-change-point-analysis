import React from 'react';
import {
    Card,
    CardContent,
    Typography,
    Chip,
    Box,
    IconButton,
    Tooltip
} from '@mui/material';
import {
    Warning,
    Policy,
    TrendingDown,
    CrisisAlert,
    Info,
    CalendarToday
} from '@mui/icons-material';

const EventsTimeline = ({ events, onEventSelect, selectedEvent }) => {
    // Get icon based on event type
    const getEventIcon = (eventType) => {
        switch (eventType) {
            case 'Geopolitical Conflict':
                return <CrisisAlert color="error" fontSize="small" />;
            case 'OPEC Policy':
                return <Policy color="success" fontSize="small" />;
            case 'Economic':
                return <TrendingDown color="warning" fontSize="small" />;
            default:
                return <Warning color="info" fontSize="small" />;
        }
    };

    // Get color based on severity
    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'Very High': return 'error';
            case 'High': return 'warning';
            case 'Medium': return 'info';
            case 'Low': return 'success';
            default: return 'default';
        }
    };

    // Sort events by date (newest first)
    const sortedEvents = [...events].sort((a, b) =>
        new Date(b.event_date) - new Date(a.event_date)
    ).slice(0, 10);

    return (
        <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Typography variant="subtitle1" gutterBottom color="primary" fontWeight="bold">
                <CalendarToday sx={{ verticalAlign: 'middle', mr: 1 }} />
                Recent Events ({events.length} total)
            </Typography>

            <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
                {sortedEvents.map((event) => (
                    <Card
                        key={event.id}
                        sx={{
                            mb: 1.5,
                            cursor: 'pointer',
                            border: selectedEvent?.id === event.id ? '2px solid #1976d2' : '1px solid #e0e0e0',
                            transition: 'all 0.2s',
                            '&:hover': {
                                boxShadow: 3,
                                borderColor: '#1976d2'
                            }
                        }}
                        onClick={() => onEventSelect(event)}
                    >
                        <CardContent sx={{ p: 1.5 }}>
                            <Box display="flex" alignItems="flex-start" gap={1}>
                                <Box sx={{ mt: 0.5 }}>
                                    {getEventIcon(event.event_type)}
                                </Box>
                                <Box sx={{ flexGrow: 1, minWidth: 0 }}>
                                    <Typography variant="body2" fontWeight="bold" noWrap>
                                        {event.event_name}
                                    </Typography>
                                    <Box display="flex" justifyContent="space-between" alignItems="center" mt={0.5}>
                                        <Typography variant="caption" color="textSecondary">
                                            {new Date(event.event_date).toLocaleDateString()}
                                        </Typography>
                                        <Box display="flex" gap={0.5}>
                                            <Chip
                                                label={event.event_type.split(' ')[0]}
                                                size="small"
                                                variant="outlined"
                                                sx={{ height: 20 }}
                                            />
                                            <Chip
                                                label={event.severity}
                                                size="small"
                                                color={getSeverityColor(event.severity)}
                                                sx={{ height: 20 }}
                                            />
                                        </Box>
                                    </Box>
                                </Box>
                                <Tooltip title="View Impact Analysis">
                                    <IconButton size="small">
                                        <Info fontSize="small" />
                                    </IconButton>
                                </Tooltip>
                            </Box>
                        </CardContent>
                    </Card>
                ))}
            </Box>

            {sortedEvents.length === 0 && (
                <Box textAlign="center" py={4}>
                    <Typography color="textSecondary">
                        No events found for selected filters
                    </Typography>
                </Box>
            )}
        </Box>
    );
};

export default EventsTimeline;