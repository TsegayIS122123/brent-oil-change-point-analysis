import React, { useState } from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    Typography,
    Box,
    Tabs,
    Tab,
    Card,
    CardContent,
    Grid,
    Chip,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    TextField,
    Switch,
    FormControlLabel,
    Alert,
    Accordion,
    AccordionSummary,
    AccordionDetails
} from '@mui/material';
import {
    Settings,
    Info,
    Code,
    Timeline,
    Security,
    DataObject,
    CloudDownload,
    Palette,
    ExpandMore,
    GitHub,
    Description,
    School,
    People,
    Build,
    Api,
    Storage,
    Analytics,
    Psychology,
    ModelTraining
} from '@mui/icons-material';

const SettingsPanel = ({ open, onClose }) => {
    const [activeTab, setActiveTab] = useState(0);
    const [settings, setSettings] = useState({
        realTimeUpdates: true,
        highContrast: false,
        autoRefresh: false,
        notifications: true,
        dataPrecision: 2,
        chartAnimation: true
    });

    const handleTabChange = (event, newValue) => {
        setActiveTab(newValue);
    };

    const handleSettingChange = (key, value) => {
        setSettings(prev => ({ ...prev, [key]: value }));
    };

    const PlatformInfo = () => (
        <Box>
            <Alert severity="info" sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom>
                    Brent Oil Intelligence Platform v1.0
                </Typography>
                <Typography variant="body2">
                    Advanced analytics platform for energy market intelligence using Bayesian statistics and machine learning.
                </Typography>
            </Alert>

            <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                    <Card variant="outlined">
                        <CardContent>
                            <Box display="flex" alignItems="center" mb={2}>
                                <Analytics sx={{ mr: 1, color: 'primary.main' }} />
                                <Typography variant="h6">Analytics Engine</Typography>
                            </Box>
                            <List dense>
                                <ListItem>
                                    <ListItemIcon><ModelTraining fontSize="small" /></ListItemIcon>
                                    <ListItemText
                                        primary="Bayesian Change Point Detection"
                                        secondary="PyMC with MCMC sampling"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemIcon><Timeline fontSize="small" /></ListItemIcon>
                                    <ListItemText
                                        primary="Time Series Analysis"
                                        secondary="ARIMA, GARCH, VAR models"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemIcon><Psychology fontSize="small" /></ListItemIcon>
                                    <ListItemText
                                        primary="Event Correlation"
                                        secondary="Cross-correlation analysis"
                                    />
                                </ListItem>
                            </List>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Card variant="outlined">
                        <CardContent>
                            <Box display="flex" alignItems="center" mb={2}>
                                <DataObject sx={{ mr: 1, color: 'primary.main' }} />
                                <Typography variant="h6">Data Pipeline</Typography>
                            </Box>
                            <List dense>
                                <ListItem>
                                    <ListItemIcon><Storage fontSize="small" /></ListItemIcon>
                                    <ListItemText
                                        primary="Data Sources"
                                        secondary="35 years of Brent crude prices + 100+ geopolitical events"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemIcon><Api fontSize="small" /></ListItemIcon>
                                    <ListItemText
                                        primary="API Integration"
                                        secondary="RESTful backend with Flask"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemIcon><CloudDownload fontSize="small" /></ListItemIcon>
                                    <ListItemText
                                        primary="Real-time Updates"
                                        secondary="Live data streaming capability"
                                    />
                                </ListItem>
                            </List>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            <Box mt={3}>
                <Typography variant="h6" gutterBottom>Methodology</Typography>
                <Accordion>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                        <Typography>Bayesian Change Point Detection</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography variant="body2" paragraph>
                            Our platform uses Markov Chain Monte Carlo (MCMC) sampling with PyMC to detect structural breaks
                            in oil price time series. The Bayesian approach provides:
                        </Typography>
                        <List dense>
                            <ListItem>
                                <ListItemText
                                    primary="Probabilistic Results"
                                    secondary="95% credible intervals for change point dates"
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="Uncertainty Quantification"
                                    secondary="Posterior distributions for all parameters"
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="Prior Knowledge Integration"
                                    secondary="Incorporate expert knowledge through informative priors"
                                />
                            </ListItem>
                        </List>
                    </AccordionDetails>
                </Accordion>

                <Accordion>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                        <Typography>Event Impact Analysis</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography variant="body2" paragraph>
                            We analyze the impact of geopolitical and economic events using:
                        </Typography>
                        <List dense>
                            <ListItem>
                                <ListItemText
                                    primary="Time-window Analysis"
                                    secondary="±30 day windows around events"
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="Statistical Significance Testing"
                                    secondary="Welch's t-tests with p-value adjustment"
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="Causal Inference"
                                    secondary="Granger causality and impulse response analysis"
                                />
                            </ListItem>
                        </List>
                    </AccordionDetails>
                </Accordion>
            </Box>
        </Box>
    );

    const TechnicalDetails = () => (
        <Box>
            <Alert severity="info" sx={{ mb: 3 }}>
                <Typography variant="body2">
                    Built with modern technologies for robust, scalable analytics.
                </Typography>
            </Alert>

            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Typography variant="subtitle1" gutterBottom fontWeight="bold">
                        Tech Stack
                    </Typography>
                </Grid>

                <Grid item xs={6} md={4}>
                    <Card variant="outlined">
                        <CardContent>
                            <Typography variant="caption" color="textSecondary">Frontend</Typography>
                            <Typography variant="body2" fontWeight="medium">React + Material-UI</Typography>
                            <Box mt={1}>
                                <Chip label="React 18" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                                <Chip label="Material-UI v5" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                                <Chip label="Recharts" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                                <Chip label="Axios" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={6} md={4}>
                    <Card variant="outlined">
                        <CardContent>
                            <Typography variant="caption" color="textSecondary">Backend</Typography>
                            <Typography variant="body2" fontWeight="medium">Flask + PyMC</Typography>
                            <Box mt={1}>
                                <Chip label="Flask" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                                <Chip label="PyMC" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                                <Chip label="Pandas" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                                <Chip label="NumPy" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={6} md={4}>
                    <Card variant="outlined">
                        <CardContent>
                            <Typography variant="caption" color="textSecondary">Data Science</Typography>
                            <Typography variant="body2" fontWeight="medium">Statistical Modeling</Typography>
                            <Box mt={1}>
                                <Chip label="Bayesian Stats" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                                <Chip label="Time Series" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                                <Chip label="Machine Learning" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                                <Chip label="Data Viz" size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            <Box mt={3}>
                <Typography variant="subtitle1" gutterBottom fontWeight="bold">
                    System Architecture
                </Typography>
                <List dense>
                    <ListItem>
                        <ListItemIcon><Build fontSize="small" /></ListItemIcon>
                        <ListItemText
                            primary="Modular Architecture"
                            secondary="Separate frontend, backend, and data layers"
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemIcon><Security fontSize="small" /></ListItemIcon>
                        <ListItemText
                            primary="Secure API"
                            secondary="CORS-enabled, input validation, rate limiting"
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemIcon><Storage fontSize="small" /></ListItemIcon>
                        <ListItemText
                            primary="Data Processing"
                            secondary="ETL pipeline with data cleaning and feature engineering"
                        />
                    </ListItem>
                    <ListItem>
                        <ListItemIcon><Code fontSize="small" /></ListItemIcon>
                        <ListItemText
                            primary="Code Quality"
                            secondary="TypeScript, ESLint, automated testing"
                        />
                    </ListItem>
                </List>
            </Box>
        </Box>
    );

    const TeamInfo = () => (
        <Box>
            <Alert severity="info" sx={{ mb: 3 }}>
                <Typography variant="body2">
                    Developed by data scientists and energy market analysts.
                </Typography>
            </Alert>

            <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                    <Card variant="outlined">
                        <CardContent>
                            <Box display="flex" alignItems="center" mb={2}>
                                <People sx={{ mr: 1, color: 'primary.main' }} />
                                <Typography variant="h6">Team</Typography>
                            </Box>
                            <List dense>
                                <ListItem>
                                    <ListItemText
                                        primary="Data Science Team"
                                        secondary="Bayesian modeling, statistical analysis, ML algorithms"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Frontend Development"
                                        secondary="React, visualization, UI/UX design"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Backend Engineering"
                                        secondary="API development, data pipeline, deployment"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Domain Experts"
                                        secondary="Energy market analysts, geopolitical researchers"
                                    />
                                </ListItem>
                            </List>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Card variant="outlined">
                        <CardContent>
                            <Box display="flex" alignItems="center" mb={2}>
                                <School sx={{ mr: 1, color: 'primary.main' }} />
                                <Typography variant="h6">Research & Development</Typography>
                            </Box>
                            <List dense>
                                <ListItem>
                                    <ListItemText
                                        primary="Academic Collaboration"
                                        secondary="Partnerships with leading universities"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Continuous Improvement"
                                        secondary="Regular model updates and validation"
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Open Source"
                                        secondary="Contributions to PyMC and data science community"
                                    />
                                </ListItem>
                            </List>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            <Box mt={3}>
                <Typography variant="subtitle1" gutterBottom fontWeight="bold">
                    Contact & Resources
                </Typography>
                <Box display="flex" gap={2} flexWrap="wrap">
                    <Button
                        variant="outlined"
                        startIcon={<GitHub />}
                        href="https://github.com/your-username/brent-oil-analysis"
                        target="_blank"
                    >
                        GitHub Repository
                    </Button>
                    <Button
                        variant="outlined"
                        startIcon={<Description />}
                        href="/api/export/pdf"
                        target="_blank"
                    >
                        Technical Documentation
                    </Button>
                    <Button
                        variant="outlined"
                        startIcon={<School />}
                        href="#"
                        onClick={(e) => {
                            e.preventDefault();
                            alert('Research papers and publications coming soon!');
                        }}
                    >
                        Research Papers
                    </Button>
                </Box>
            </Box>
        </Box>
    );

    const UserSettings = () => (
        <Box>
            <Typography variant="h6" gutterBottom>Dashboard Settings</Typography>

            <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                    <Card variant="outlined">
                        <CardContent>
                            <Typography variant="subtitle2" gutterBottom>Display Settings</Typography>

                            <FormControlLabel
                                control={
                                    <Switch
                                        checked={settings.chartAnimation}
                                        onChange={(e) => handleSettingChange('chartAnimation', e.target.checked)}
                                    />
                                }
                                label="Chart Animations"
                            />

                            <FormControlLabel
                                control={
                                    <Switch
                                        checked={settings.highContrast}
                                        onChange={(e) => handleSettingChange('highContrast', e.target.checked)}
                                    />
                                }
                                label="High Contrast Mode"
                            />

                            <Box mt={2}>
                                <Typography variant="body2" gutterBottom>Data Precision</Typography>
                                <TextField
                                    select
                                    size="small"
                                    value={settings.dataPrecision}
                                    onChange={(e) => handleSettingChange('dataPrecision', parseInt(e.target.value))}
                                    fullWidth
                                    SelectProps={{
                                        native: true,
                                    }}
                                >
                                    <option value={0}>0 decimal places</option>
                                    <option value={1}>1 decimal place</option>
                                    <option value={2}>2 decimal places</option>
                                    <option value={3}>3 decimal places</option>
                                </TextField>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Card variant="outlined">
                        <CardContent>
                            <Typography variant="subtitle2" gutterBottom>Data & Updates</Typography>

                            <FormControlLabel
                                control={
                                    <Switch
                                        checked={settings.realTimeUpdates}
                                        onChange={(e) => handleSettingChange('realTimeUpdates', e.target.checked)}
                                    />
                                }
                                label="Real-time Data Updates"
                            />

                            <FormControlLabel
                                control={
                                    <Switch
                                        checked={settings.autoRefresh}
                                        onChange={(e) => handleSettingChange('autoRefresh', e.target.checked)}
                                    />
                                }
                                label="Auto-refresh (every 5 min)"
                                disabled={!settings.realTimeUpdates}
                            />

                            <FormControlLabel
                                control={
                                    <Switch
                                        checked={settings.notifications}
                                        onChange={(e) => handleSettingChange('notifications', e.target.checked)}
                                    />
                                }
                                label="Desktop Notifications"
                            />
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            <Box mt={3}>
                <Typography variant="subtitle2" gutterBottom>Color Theme</Typography>
                <Box display="flex" gap={2}>
                    <Chip
                        label="Light"
                        onClick={() => console.log('Set light theme')}
                        variant="outlined"
                        icon={<Palette />}
                    />
                    <Chip
                        label="Dark"
                        onClick={() => console.log('Set dark theme')}
                        variant="outlined"
                        icon={<Palette />}
                    />
                    <Chip
                        label="Blue"
                        onClick={() => console.log('Set blue theme')}
                        variant="outlined"
                        icon={<Palette />}
                    />
                </Box>
            </Box>
        </Box>
    );

    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
            <DialogTitle>
                <Box display="flex" alignItems="center">
                    <Settings sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="h6">Platform Settings & Information</Typography>
                </Box>
            </DialogTitle>

            <DialogContent>
                <Tabs
                    value={activeTab}
                    onChange={handleTabChange}
                    variant="fullWidth"
                    sx={{ mb: 3 }}
                >
                    <Tab icon={<Info />} label="Platform Info" />
                    <Tab icon={<Code />} label="Technical Details" />
                    <Tab icon={<People />} label="Team & Research" />
                    <Tab icon={<Settings />} label="User Settings" />
                </Tabs>

                <Box sx={{ mt: 2 }}>
                    {activeTab === 0 && <PlatformInfo />}
                    {activeTab === 1 && <TechnicalDetails />}
                    {activeTab === 2 && <TeamInfo />}
                    {activeTab === 3 && <UserSettings />}
                </Box>
            </DialogContent>

            <DialogActions sx={{ p: 3, pt: 0 }}>
                <Button onClick={onClose} color="primary">
                    Close
                </Button>
                <Button
                    variant="contained"
                    onClick={() => {
                        // Save settings to localStorage or backend
                        localStorage.setItem('brentOilSettings', JSON.stringify(settings));
                        onClose();
                    }}
                >
                    Save Settings
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default SettingsPanel;