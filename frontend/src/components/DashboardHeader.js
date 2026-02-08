import React from 'react';
import { AppBar, Toolbar, Typography, Box, Button, Chip, IconButton, Menu, MenuItem } from '@mui/material';
import {
    Timeline, CloudDownload, Refresh, Settings, MoreVert
} from '@mui/icons-material';

const DashboardHeader = ({ onExport, onRefresh, activeTab }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);

    const handleMenuClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
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

                    <IconButton
                        color="inherit"
                        size="large"
                        onClick={() => alert('Settings would open here')}
                        sx={{ fontSize: '1.5rem' }}
                    >
                        <Settings />
                    </IconButton>

                    <Button
                        color="inherit"
                        variant="outlined"
                        startIcon={<CloudDownload />}
                        onClick={onExport}
                        size="large"
                        sx={{ fontSize: '1rem', px: 2 }}
                    >
                        Export Report
                    </Button>

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
                        <MenuItem onClick={() => { handleMenuClose(); onExport(); }}>
                            <CloudDownload sx={{ mr: 1 }} /> Export Report
                        </MenuItem>
                        <MenuItem onClick={() => { handleMenuClose(); alert('Settings opened'); }}>
                            <Settings sx={{ mr: 1 }} /> Settings
                        </MenuItem>
                    </Menu>
                </Box>
            </Toolbar>
        </AppBar>
    );
};

export default DashboardHeader;