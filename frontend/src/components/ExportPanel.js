import React from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    FormControl,
    FormLabel,
    RadioGroup,
    FormControlLabel,
    Radio,
    TextField,
    Box,
    Typography,
    Divider,
    Chip
} from '@mui/material';
import {
    Download,
    PictureAsPdf,
    InsertChart,
    Description
} from '@mui/icons-material';

const ExportPanel = ({ open, onClose }) => {
    const [format, setFormat] = React.useState('pdf');
    const [range, setRange] = React.useState('current');

    return (
        <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
            <DialogTitle>
                <Box display="flex" alignItems="center">
                    <Download sx={{ mr: 1 }} />
                    Export Analysis Report
                </Box>
            </DialogTitle>
            <DialogContent>
                <Box mb={3}>
                    <Typography variant="body2" color="textSecondary">
                        Generate comprehensive reports for stakeholders
                    </Typography>
                </Box>

                <FormControl component="fieldset" sx={{ mb: 3 }}>
                    <FormLabel component="legend">Report Format</FormLabel>
                    <RadioGroup
                        value={format}
                        onChange={(e) => setFormat(e.target.value)}
                        row
                    >
                        <FormControlLabel
                            value="pdf"
                            control={<Radio />}
                            label={
                                <Box display="flex" alignItems="center">
                                    <PictureAsPdf sx={{ mr: 1 }} fontSize="small" />
                                    PDF Document
                                </Box>
                            }
                        />
                        <FormControlLabel
                            value="excel"
                            control={<Radio />}
                            label={
                                <Box display="flex" alignItems="center">
                                    <InsertChart sx={{ mr: 1 }} fontSize="small" />
                                    Excel Data
                                </Box>
                            }
                        />
                        <FormControlLabel
                            value="presentation"
                            control={<Radio />}
                            label={
                                <Box display="flex" alignItems="center">
                                    <Description sx={{ mr: 1 }} fontSize="small" />
                                    Presentation
                                </Box>
                            }
                        />
                    </RadioGroup>
                </FormControl>

                <FormControl component="fieldset" fullWidth sx={{ mb: 3 }}>
                    <FormLabel component="legend">Data Range</FormLabel>
                    <RadioGroup
                        value={range}
                        onChange={(e) => setRange(e.target.value)}
                    >
                        <FormControlLabel value="current" control={<Radio />} label="Current View" />
                        <FormControlLabel value="full" control={<Radio />} label="Full History (1987-2022)" />
                        <FormControlLabel value="custom" control={<Radio />} label="Custom Range" />
                    </RadioGroup>
                </FormControl>

                {range === 'custom' && (
                    <Box mb={3}>
                        <TextField
                            label="Start Date"
                            type="date"
                            fullWidth
                            InputLabelProps={{ shrink: true }}
                            sx={{ mb: 2 }}
                        />
                        <TextField
                            label="End Date"
                            type="date"
                            fullWidth
                            InputLabelProps={{ shrink: true }}
                        />
                    </Box>
                )}

                <Divider sx={{ my: 2 }} />

                <Box>
                    <Typography variant="subtitle2" gutterBottom>
                        Included Sections:
                    </Typography>
                    <Box display="flex" flexWrap="wrap" gap={1} mb={2}>
                        <Chip label="Price Analysis" size="small" />
                        <Chip label="Event Correlation" size="small" color="primary" />
                        <Chip label="Change Point Detection" size="small" />
                        <Chip label="Volatility Metrics" size="small" />
                        <Chip label="Predictive Insights" size="small" color="secondary" />
                    </Box>
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button variant="contained" startIcon={<Download />}>
                    Generate Report
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ExportPanel;