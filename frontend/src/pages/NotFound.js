import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Button, Box, Paper } from '@mui/material';
import { Home as HomeIcon } from '@mui/icons-material';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 8, textAlign: 'center' }}>
        <Paper elevation={3} sx={{ p: 5 }}>
          <Typography variant="h1" component="h1" sx={{ fontSize: '6rem', fontWeight: 'bold', color: '#1976d2' }}>
            404
          </Typography>
          <Typography variant="h4" component="h2" gutterBottom>
            页面未找到
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            抱歉，您访问的页面不存在或已被移除。
          </Typography>
          <Button
            variant="contained"
            startIcon={<HomeIcon />}
            onClick={() => navigate('/')}
            sx={{ mt: 2 }}
          >
            返回首页
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};

export default NotFound; 