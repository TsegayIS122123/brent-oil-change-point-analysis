import React from 'react';
import { AppBar, Toolbar, Typography, Box, Button, Chip, IconButton, Menu, MenuItem, Dialog, DialogTitle, DialogContent, DialogActions, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import {
    Timeline, Refresh, Settings, MoreVert, Info, Help,
    School, Psychology, DataObject, Analytics, Code, People
} from '@mui/icons-material';

const DashboardHeader = ({ onSettings, onRefresh, activeTab }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [aboutOpen, setAboutOpen] = React.useState(false); // NEW STATE
    const open = Boolean(anchorEl);

    const handleMenuClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    const handleAboutClick = () => {
        handleMenuClose();
        setAboutOpen(true);
    };

    const handleAboutClose = () => {
        setAboutOpen(false);
    };

    const getTabTitle = () => {
        switch (activeTab) {
            case 0: return 'Dashboard Overview';
            case 1: return 'Statistical Analytics';
            case 2: return 'Predictive Insights';
            case 3: return 'Events Analysis';
            default: return 'Brent Oil Intelligence Platform';
        }
    };

    return (
        <>
            <AppBar position="static" color="primary" elevation={3}>
                <Toolbar>
                    <Box display="flex" alignItems="center" flexGrow={1}>
                        <Timeline sx={{ mr: 2, fontSize: '2rem' }} />
                        <Box>
                            <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                                Brent Oil Intelligence Platform
                            </Typography>
                            <Typography variant="subtitle1" sx={{ opacity: 0.9, fontSize: '1rem' }}>
                                {getTabTitle()}
                            </Typography>
                        </Box>
                    </Box>

                    <Box display="flex" alignItems="center" gap={2}>
                        <Chip
                            label="Bayesian Analysis"
                            color="secondary"
                            size="medium"
                            sx={{ fontSize: '0.875rem' }}
                        />
                        <Chip
                            label="Real-time"
                            color="success"
                            size="medium"
                            variant="outlined"
                            sx={{ fontSize: '0.875rem' }}
                        />

                        {/* Settings Button */}
                        <IconButton
                            color="inherit"
                            size="large"
                            onClick={onSettings}
                            sx={{ fontSize: '1.5rem' }}
                            title="Platform Settings & Information"
                        >
                            <Settings />
                        </IconButton>

                        {/* Refresh Button */}
                        <Button
                            color="inherit"
                            variant="outlined"
                            startIcon={<Refresh />}
                            onClick={onRefresh}
                            size="large"
                            sx={{ fontSize: '1rem', px: 2 }}
                        >
                            Refresh Data
                        </Button>

                        {/* Menu for additional options */}
                        <IconButton
                            color="inherit"
                            size="large"
                            onClick={handleMenuClick}
                        >
                            <MoreVert />
                        </IconButton>

                        <Menu
                            anchorEl={anchorEl}
                            open={open}
                            onClose={handleMenuClose}
                        >
                            <MenuItem onClick={() => { handleMenuClose(); onRefresh(); }}>
                                <Refresh sx={{ mr: 1 }} /> Refresh Data
                            </MenuItem>
                            <MenuItem onClick={() => { handleMenuClose(); onSettings(); }}>
                                <Settings sx={{ mr: 1 }} /> Settings & Info
                            </MenuItem>
                            <MenuItem onClick={() => { handleMenuClose(); window.open('https://github.com/TsegayIS122123/brent-oil-change-point-analysis', '_blank'); }}>
                                <Help sx={{ mr: 1 }} /> Documentation (GitHub)
                            </MenuItem>
                            <MenuItem onClick={handleAboutClick}>
                                <Info sx={{ mr: 1 }} /> About This Project
                            </MenuItem>
                        </Menu>
                    </Box>
                </Toolbar>
            </AppBar>

            {/* About Dialog */}
            <Dialog open={aboutOpen} onClose={handleAboutClose} maxWidth="sm" fullWidth>
                <DialogTitle>
                    <Box display="flex" alignItems="center">
                        <Info sx={{ mr: 1, color: 'primary.main' }} />
                        About Brent Oil Intelligence Platform
                    </Box>
                </DialogTitle>
                <DialogContent>
                    <Typography variant="body1" paragraph>
                        <strong>An advanced analytics platform</strong> for understanding how geopolitical events impact Brent Crude Oil prices using Bayesian statistics and machine learning.
                    </Typography>

                    <List dense>
                        <ListItem>
                            <ListItemIcon><Psychology fontSize="small" /></ListItemIcon>
                            <ListItemText
                                primary="Bayesian Change Point Detection"
                                secondary="Identifying structural breaks in oil prices"
                            />
                        </ListItem>
                        <ListItem>
                            <ListItemIcon><Analytics fontSize="small" /></ListItemIcon>
                            <ListItemText
                                primary="Event Correlation Analysis"
                                secondary="Quantifying impact of geopolitical events"
                            />
                        </ListItem>
                        <ListItem>
                            <ListItemIcon><DataObject fontSize="small" /></ListItemIcon>
                            <ListItemText
                                primary="35 Years of Historical Data"
                                secondary="1987-2022 daily Brent prices"
                            />
                        </ListItem>
                        <ListItem>
                            <ListItemIcon><Code fontSize="small" /></ListItemIcon>
                            <ListItemText
                                primary="Full-stack Implementation"
                                secondary="React frontend + Flask backend + PyMC"
                            />
                        </ListItem>
                        <ListItem>
                            <ListItemIcon><School fontSize="small" /></ListItemIcon>
                            <ListItemText
                                primary="Academic Project"
                                secondary="Data Science Internship Challenge"
                            />
                        </ListItem>
                        <ListItem>
                            <ListItemIcon><People fontSize="small" /></ListItemIcon>
                            <ListItemText
                                primary="By Tsegay"
                                secondary="Portfolio Project"
                            />
                        </ListItem>
                    </List>

                    <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
                        <strong>Technologies:</strong> React, Material-UI, Flask, PyMC, Pandas, Recharts
                    </Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleAboutClose}>Close</Button>
                    <Button
                        variant="contained"
                        onClick={() => {
                            handleAboutClose();
                            window.open('https://github.com/TsegayIS122123/brent-oil-change-point-analysis', '_blank');
                        }}
                    >
                        View GitHub
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
};

export default DashboardHeader;