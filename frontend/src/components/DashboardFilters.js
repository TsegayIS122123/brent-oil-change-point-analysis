import React from 'react';

import {
    Grid,
    TextField,
    Button,
    Alert,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Box,
    Typography
} from '@mui/material';
import { FilterList, Refresh } from '@mui/icons-material';

const DashboardFilters = ({ filters, onFilterChange, onRefresh, dataStats }) => {
    return (
        <Box sx={{ p: 2, borderRadius: 2, bgcolor: 'background.paper' }}>
            <Grid container spacing={2} alignItems="center">
                <Grid item xs={12} md={2}>
                    <FormControl fullWidth>
                        <InputLabel><FilterList fontSize="small" /> Event Type</InputLabel>
                        <Select
                            value={filters.eventType}
                            label="Event Type"
                            onChange={(e) => onFilterChange('eventType', e.target.value)}
                        >
                            <MenuItem value="all">All Types</MenuItem>
                            <MenuItem value="Geopolitical Conflict">Geopolitical</MenuItem>
                            <MenuItem value="OPEC Policy">OPEC Policy</MenuItem>
                            <MenuItem value="Economic">Economic</MenuItem>
                            <MenuItem value="Economic Sanctions">Sanctions</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>

                <Grid item xs={12} md={2}>
                    <FormControl fullWidth>
                        <InputLabel>Severity</InputLabel>
                        <Select
                            value={filters.severity}
                            label="Severity"
                            onChange={(e) => onFilterChange('severity', e.target.value)}
                        >
                            <MenuItem value="all">All Severities</MenuItem>
                            <MenuItem value="Very High">Very High</MenuItem>
                            <MenuItem value="High">High</MenuItem>
                            <MenuItem value="Medium">Medium</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>

                <Grid item xs={12} md={2}>
                    <TextField
                        fullWidth
                        label="Start Date"
                        type="date"
                        value={filters.startDate}
                        onChange={(e) => onFilterChange('startDate', e.target.value)}
                        InputLabelProps={{ shrink: true }}
                    />
                </Grid>

                <Grid item xs={12} md={2}>
                    <TextField
                        fullWidth
                        label="End Date"
                        type="date"
                        value={filters.endDate}
                        onChange={(e) => onFilterChange('endDate', e.target.value)}
                        InputLabelProps={{ shrink: true }}
                    />
                </Grid>

                <Grid item xs={12} md={2}>
                    <Button
                        variant="contained"
                        fullWidth
                        startIcon={<Refresh />}
                        onClick={onRefresh}
                        sx={{ height: '56px' }}
                    >
                        Refresh Data
                    </Button>
                </Grid>

                <Grid item xs={12} md={2}>
                    <Alert severity="info" icon={false}>
                        <Typography variant="caption">
                            {dataStats?.priceCount || 0} prices, {dataStats?.eventCount || 0} events
                        </Typography>
                    </Alert>
                </Grid>
            </Grid>
        </Box>
    );
};

export default DashboardFilters;