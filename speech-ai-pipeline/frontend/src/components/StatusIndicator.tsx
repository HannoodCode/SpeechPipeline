import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Chip,
  Button,
  Grid,
} from '@mui/material';
import {
  CheckCircle,
  Error,
  Refresh,
} from '@mui/icons-material';
import { PipelineStatus } from '../types';

interface StatusIndicatorProps {
  status: PipelineStatus | null;
  onRefresh: () => void;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  status,
  onRefresh,
}) => {
  const getStatusIcon = (isAvailable: boolean) => {
    return isAvailable ? (
      <CheckCircle sx={{ color: 'success.main', fontSize: 20 }} />
    ) : (
      <Error sx={{ color: 'error.main', fontSize: 20 }} />
    );
  };

  const getStatusColor = (isAvailable: boolean): "success" | "error" => {
    return isAvailable ? "success" : "error";
  };

  if (!status) {
    return (
      <Paper sx={{ p: 2, bgcolor: 'warning.light' }}>
        <Typography variant="body2" sx={{ color: 'rgba(0,0,0,0.87)' }}>
          Loading service status...
        </Typography>
      </Paper>
    );
  }

  const serviceCategories = [
    { key: 'stt', label: 'Speech-to-Text', services: status.stt },
    { key: 'llm', label: 'Language Models', services: status.llm },
    { key: 'tts', label: 'Text-to-Speech', services: status.tts },
  ];

  return (
    <Paper sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">
          Service Status
        </Typography>
        <Button
          variant="outlined"
          size="small"
          onClick={onRefresh}
          startIcon={<Refresh />}
        >
          Refresh
        </Button>
      </Box>

      <Grid container spacing={2}>
        {serviceCategories.map(({ key, label, services }) => (
          <Grid item xs={12} md={4} key={key}>
            <Typography variant="subtitle2" gutterBottom>
              {label}
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              {Object.entries(services).map(([serviceName, isAvailable]) => (
                <Box
                  key={serviceName}
                  sx={{ display: 'flex', alignItems: 'center', gap: 1 }}
                >
                  {getStatusIcon(isAvailable)}
                  <Chip
                    label={serviceName.toUpperCase()}
                    color={getStatusColor(isAvailable)}
                    variant={isAvailable ? "filled" : "outlined"}
                    size="small"
                  />
                </Box>
              ))}
            </Box>
          </Grid>
        ))}
      </Grid>

      {/* Overall Status Summary */}
      <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid', borderColor: 'divider' }}>
        <Typography variant="body2" color="text.secondary">
           Services marked with ❌ require API keys or additional setup. 
          Check the README for configuration instructions.
        </Typography>
      </Box>
    </Paper>
  );
}; 