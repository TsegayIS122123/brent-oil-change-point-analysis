import React from 'react';
import {
    Paper,
    Typography,
    Box,
    Grid,
    Card,
    CardContent,
    Chip,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Divider
} from '@mui/material';
import {
    TrendingUp,
    TrendingDown,
    Warning,
    Lightbulb,
    Timeline,
    ShowChart,
    Psychology
} from '@mui/icons-material';

const PredictiveInsights = () => {
    const insights = [
        {
            title: 'Regime Shift Detection',
            description: 'Market transitioning to higher volatility regime',
            confidence: 85,
            impact: 'High',
            trend: 'up'
        },
        {
            title: 'OPEC Meeting Impact',
            description: 'Expected 5-8% price movement based on historical patterns',
            confidence: 78,
            impact: 'Medium',
            trend: 'up'
        },
        {
            title: 'Seasonal Pattern',
            description: 'Q4 typically shows 12% higher prices than Q2',
            confidence: 92,
            impact: 'Medium',
            trend: 'up'
        },
        {
            title: 'Geopolitical Risk',
            description: 'Elevated Middle East tensions suggest 15% upside risk',
            confidence: 65,
            impact: 'High',
            trend: 'up'
        }
    ];

    return (
        <Box>
            <Box display="flex" alignItems="center" mb={3}>
                <Psychology sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">
                    AI-Powered Predictive Insights
                </Typography>
                <Chip label="ML Model" size="small" sx={{ ml: 2 }} />
            </Box>

            <Grid container spacing={3}>
                {insights.map((insight, index) => (
                    <Grid item xs={12} md={6} key={index}>
                        <Card
                            sx={{
                                height: '100%',
                                borderLeft: `4px solid ${insight.trend === 'up' ? '#00c853' : '#ff4444'}`,
                                transition: 'transform 0.2s',
                                '&:hover': {
                                    transform: 'translateY(-4px)'
                                }
                            }}
                        >
                            <CardContent>
                                <Box display="flex" justifyContent="space-between" alignItems="start" mb={2}>
                                    <Box>
                                        <Typography variant="h6" gutterBottom>
                                            {insight.title}
                                        </Typography>
                                        <Typography variant="body2" color="textSecondary">
                                            {insight.description}
                                        </Typography>
                                    </Box>
                                    {insight.trend === 'up' ? (
                                        <TrendingUp color="success" />
                                    ) : (
                                        <TrendingDown color="error" />
                                    )}
                                </Box>

                                <Box display="flex" justifyContent="space-between" alignItems="center" mt={2}>
                                    <Box>
                                        <Chip
                                            label={`${insight.confidence}% confidence`}
                                            size="small"
                                            color={insight.confidence > 80 ? "success" : "warning"}
                                            variant="outlined"
                                        />
                                    </Box>
                                    <Box>
                                        <Chip
                                            label={insight.impact}
                                            size="small"
                                            color={insight.impact === 'High' ? "error" : "warning"}
                                        />
                                    </Box>
                                </Box>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            <Paper sx={{ p: 2, mt: 3 }}>
                <Typography variant="subtitle2" gutterBottom color="textSecondary">
                    <Lightbulb sx={{ verticalAlign: 'middle', mr: 1 }} fontSize="small" />
                    Key Recommendations
                </Typography>
                <List dense>
                    <ListItem>
                        <ListItemIcon>
                            <ShowChart fontSize="small" />
                        </ListItemIcon>
                        <ListItemText
                            primary="Increase hedging positions given elevated volatility forecasts"
                            secondary="Based on GARCH volatility model projections"
                        />
                    </ListItem>
                    <Divider component="li" />
                    <ListItem>
                        <ListItemIcon>
                            <Timeline fontSize="small" />
                        </ListItemIcon>
                        <ListItemText
                            primary="Consider tactical long positions ahead of seasonal uptrend"
                            secondary="Historical pattern shows 73% probability of Q4 rally"
                        />
                    </ListItem>
                    <Divider component="li" />
                    <ListItem>
                        <ListItemIcon>
                            <Warning fontSize="small" />
                        </ListItemIcon>
                        <ListItemText
                            primary="Monitor OPEC+ meetings for policy shift signals"
                            secondary="Next meeting scheduled for November 30, 2024"
                        />
                    </ListItem>
                </List>
            </Paper>
        </Box>
    );
};

export default PredictiveInsights;