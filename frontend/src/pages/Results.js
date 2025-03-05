import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  Divider,
  Grid,
  List,
  ListItem,
  ListItemText,
  Chip,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Home as HomeIcon,
  Refresh as RefreshIcon,
  Check as CheckIcon,
  Close as CloseIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import axios from 'axios';

const Results = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [session, setSession] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [evaluation, setEvaluation] = useState(null);

  // 加载会话信息和答案
  useEffect(() => {
    const sessionData = localStorage.getItem('interviewSession');
    const answersData = localStorage.getItem('interviewAnswers');
    
    if (!sessionData || !answersData) {
      navigate('/');
      return;
    }
    
    try {
      const parsedSession = JSON.parse(sessionData);
      const parsedAnswers = JSON.parse(answersData);
      
      setSession(parsedSession);
      setAnswers(parsedAnswers);
      
      // 获取评估结果
      fetchEvaluation(parsedSession.interview_id);
    } catch (err) {
      console.error('解析数据失败:', err);
      setError('无法加载面试数据');
      setLoading(false);
    }
  }, [navigate]);

  // 获取评估结果
  const fetchEvaluation = async (interviewId) => {
    setLoading(true);
    setError('');

    try {
      const response = await axios.get(`/api/interview/evaluate?interview_id=${interviewId}`);
      
      if (response.data.status === 'success') {
        setEvaluation(response.data.data);
      } else {
        setError(response.data.message || '获取评估结果失败');
      }
    } catch (err) {
      console.error('获取评估请求失败:', err);
      setError('网络错误，请检查您的连接');
    } finally {
      setLoading(false);
    }
  };

  // 重新开始面试
  const handleRestart = () => {
    localStorage.removeItem('interviewSession');
    localStorage.removeItem('interviewAnswers');
    navigate('/setup');
  };

  // 返回首页
  const handleHome = () => {
    localStorage.removeItem('interviewSession');
    localStorage.removeItem('interviewAnswers');
    navigate('/');
  };

  // 渲染评分组件
  const renderScore = (score) => {
    let color = 'error';
    if (score >= 80) color = 'success';
    else if (score >= 60) color = 'warning';
    
    return (
      <Box sx={{ position: 'relative', display: 'inline-flex' }}>
        <CircularProgress
          variant="determinate"
          value={score}
          color={color}
          size={80}
          thickness={5}
        />
        <Box
          sx={{
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            position: 'absolute',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Typography variant="h5" component="div" color="text.secondary">
            {score}
          </Typography>
        </Box>
      </Box>
    );
  };

  if (loading) {
    return (
      <Container maxWidth="md">
        <Box sx={{ my: 8, textAlign: 'center' }}>
          <CircularProgress />
          <Typography variant="h6" sx={{ mt: 2 }}>
            正在生成面试评估...
          </Typography>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          面试评估结果
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {evaluation && (
          <>
            <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={4} sx={{ textAlign: 'center' }}>
                  <Typography variant="h6" gutterBottom>
                    总体评分
                  </Typography>
                  {renderScore(evaluation.score)}
                </Grid>
                <Grid item xs={12} md={8}>
                  <Typography variant="h6" gutterBottom>
                    评估总结
                  </Typography>
                  <Typography variant="body1" paragraph>
                    {evaluation.summary}
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="subtitle1" gutterBottom>
                    建议
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {evaluation.suggestions}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>

            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      优势
                    </Typography>
                    <List dense>
                      {evaluation.strengths.map((strength, index) => (
                        <ListItem key={index}>
                          <CheckIcon color="success" sx={{ mr: 1 }} />
                          <ListItemText primary={strength} />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      需要改进
                    </Typography>
                    <List dense>
                      {evaluation.weaknesses.map((weakness, index) => (
                        <ListItem key={index}>
                          <InfoIcon color="error" sx={{ mr: 1 }} />
                          <ListItemText primary={weakness} />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Typography variant="h5" gutterBottom>
              问答详情
            </Typography>
            {answers.map((item, index) => (
              <Accordion key={index} sx={{ mb: 2 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography>
                    问题 {index + 1}: {item.question.content.substring(0, 60)}...
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="subtitle1" gutterBottom>
                    问题:
                  </Typography>
                  <Typography variant="body1" paragraph>
                    {item.question.content}
                  </Typography>
                  
                  <Typography variant="subtitle1" gutterBottom>
                    您的回答:
                  </Typography>
                  <Typography variant="body1" paragraph>
                    {item.content}
                  </Typography>
                  
                  {item.analysis && (
                    <>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="subtitle1" gutterBottom>
                        回答质量:
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <Box sx={{ width: '100%', mr: 1 }}>
                          <LinearProgress 
                            variant="determinate" 
                            value={item.analysis.quality * 100} 
                            color={item.analysis.quality > 0.7 ? "success" : item.analysis.quality > 0.4 ? "warning" : "error"}
                          />
                        </Box>
                        <Box sx={{ minWidth: 35 }}>
                          <Typography variant="body2" color="text.secondary">
                            {Math.round(item.analysis.quality * 100)}%
                          </Typography>
                        </Box>
                      </Box>
                      
                      <Typography variant="subtitle1" gutterBottom>
                        反馈:
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {item.analysis.feedback}
                      </Typography>
                    </>
                  )}
                </AccordionDetails>
              </Accordion>
            ))}
          </>
        )}

        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
          <Button
            variant="outlined"
            startIcon={<HomeIcon />}
            onClick={handleHome}
          >
            返回首页
          </Button>
          <Button
            variant="contained"
            startIcon={<RefreshIcon />}
            onClick={handleRestart}
          >
            再次面试
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default Results; 