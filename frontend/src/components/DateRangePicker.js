import React, { useState } from 'react';
import {
    Box,
    TextField,
    Button,
    Popover,
    Typography
} from '@mui/material';
import { DateRange as DateRangeIcon } from '@mui/icons-material';

const DateRangePicker = ({ startDate, endDate, onDateChange }) => {
    const [anchorEl, setAnchorEl] = useState(null);
    const [tempStart, setTempStart] = useState(startDate);
    const [tempEnd, setTempEnd] = useState(endDate);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleApply = () => {
        onDateChange(tempStart, tempEnd);
        handleClose();
    };

    const open = Boolean(anchorEl);

    return (
        <Box>
            <Button
                variant="outlined"
                startIcon={<DateRangeIcon />}
                onClick={handleClick}
                fullWidth
                sx={{ justifyContent: 'flex-start' }}
            >
                {startDate} to {endDate}
            </Button>

            <Popover
                open={open}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left',
                }}
            >
                <Box sx={{ p: 2, width: 300 }}>
                    <Typography variant="subtitle1" gutterBottom>
                        Select Date Range
                    </Typography>

                    <TextField
                        fullWidth
                        label="Start Date"
                        type="date"
                        value={tempStart}
                        onChange={(e) => setTempStart(e.target.value)}
                        InputLabelProps={{ shrink: true }}
                        sx={{ mb: 2 }}
                    />

                    <TextField
                        fullWidth
                        label="End Date"
                        type="date"
                        value={tempEnd}
                        onChange={(e) => setTempEnd(e.target.value)}
                        InputLabelProps={{ shrink: true }}
                        sx={{ mb: 2 }}
                    />

                    <Box display="flex" justifyContent="space-between">
                        <Button onClick={handleClose} color="inherit">
                            Cancel
                        </Button>
                        <Button variant="contained" onClick={handleApply}>
                            Apply
                        </Button>
                    </Box>
                </Box>
            </Popover>
        </Box>
    );
};

export default DateRangePicker;