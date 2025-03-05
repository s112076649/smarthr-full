import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Container, 
  Typography, 
  Button, 
  Box, 
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import { 
  PlayArrow as PlayIcon,
  School as SchoolIcon,
  Psychology as PsychologyIcon,
  RecordVoiceOver as VoiceIcon,
  Translate as TranslateIcon,
  Analytics as AnalyticsIcon
} from '@mui/icons-material';

const Home = () => {
  const navigate = useNavigate();

  const handleStartClick = () => {
    navigate('/setup');
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom>
          AI面试模拟系统
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          使用人工智能技术提升您的面试技巧，随时随地进行模拟面试练习
        </Typography>
        <Button 
          variant="contained" 
          size="large" 
          startIcon={<PlayIcon />}
          onClick={handleStartClick}
          sx={{ mt: 3, mb: 5, py: 1.5, px: 4, fontSize: '1.2rem' }}
        >
          开始面试
        </Button>
      </Box>

      <Grid container spacing={4} sx={{ mb: 6 }}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <SchoolIcon color="primary" sx={{ fontSize: 40, mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                多行业面试场景
              </Typography>
              <Typography variant="body1" color="text.secondary">
                支持软件工程师、产品经理、数据科学家等多种职位的面试模拟，针对不同公司和岗位定制问题。
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <PsychologyIcon color="primary" sx={{ fontSize: 40, mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                机器学习优化
              </Typography>
              <Typography variant="body1" color="text.secondary">
                系统会根据您的回答自动调整问题难度和方向，提供个性化的面试体验，帮助您更有效地提升能力。
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <VoiceIcon color="primary" sx={{ fontSize: 40, mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                语音交互
              </Typography>
              <Typography variant="body1" color="text.secondary">
                支持语音识别和合成，让面试过程更加自然流畅，模拟真实面试场景，提升口语表达能力。
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper elevation={3} sx={{ p: 4, mb: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          为什么选择我们的AI面试系统？
        </Typography>
        <List>
          <ListItem>
            <ListItemIcon><AnalyticsIcon color="primary" /></ListItemIcon>
            <ListItemText 
              primary="专业评估反馈" 
              secondary="每次面试后获得详细的评估报告，包括优势、不足和改进建议，帮助您持续提升" 
            />
          </ListItem>
          <ListItem>
            <ListItemIcon><TranslateIcon color="primary" /></ListItemIcon>
            <ListItemText 
              primary="多语言支持" 
              secondary="支持中英文面试，满足不同语言环境的面试需求" 
            />
          </ListItem>
          <ListItem>
            <ListItemIcon><SchoolIcon color="primary" /></ListItemIcon>
            <ListItemText 
              primary="随时随地练习" 
              secondary="Web应用支持各种设备访问，您可以在任何时间、任何地点进行面试练习" 
            />
          </ListItem>
        </List>
      </Paper>

      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          准备好提升您的面试技巧了吗？
        </Typography>
        <Button 
          variant="contained" 
          size="large" 
          startIcon={<PlayIcon />}
          onClick={handleStartClick}
          sx={{ mt: 2, py: 1.5, px: 4, fontSize: '1.2rem' }}
        >
          立即开始
        </Button>
      </Box>
    </Container>
  );
};

export default Home; 