import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  Button,
  Grid,
  CircularProgress,
  Alert,
  Divider
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  PlayArrow as StartIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';
import axios from 'axios';

const Setup = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [interviewTypes, setInterviewTypes] = useState({});
  
  // 面试设置状态
  const [formData, setFormData] = useState({
    type: 'software_engineer',
    company: '',
    language: 'zh',
    useML: true
  });

  // 获取面试类型
  useEffect(() => {
    const fetchInterviewTypes = async () => {
      try {
        const response = await axios.get('/api/interview/types');
        if (response.data.status === 'success') {
          setInterviewTypes(response.data.data);
        }
      } catch (err) {
        console.error('获取面试类型失败:', err);
        // 使用默认面试类型
        setInterviewTypes({
          'software_engineer': '软件工程师',
          'product_manager': '产品经理',
          'data_scientist': '数据科学家',
          'frontend_developer': '前端开发工程师',
          'backend_developer': '后端开发工程师'
        });
      }
    };

    fetchInterviewTypes();
  }, []);

  // 处理表单变化
  const handleChange = (e) => {
    const { name, value, checked } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'useML' ? checked : value
    });
  };

  // 开始面试
  const handleStartInterview = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/interview/start', {
        type: formData.type,
        company: formData.company || '通用公司',
        language: formData.language,
        use_ml: formData.useML
      });

      if (response.data.status === 'success') {
        // 保存面试会话信息到本地存储
        localStorage.setItem('interviewSession', JSON.stringify(response.data.data));
        // 导航到面试页面
        navigate('/interview');
      } else {
        setError(response.data.message || '开始面试失败，请重试');
      }
    } catch (err) {
      console.error('开始面试请求失败:', err);
      setError('网络错误，请检查您的连接并重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Button
          startIcon={<BackIcon />}
          onClick={() => navigate('/')}
          sx={{ mb: 2 }}
        >
          返回首页
        </Button>

        <Paper elevation={3} sx={{ p: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <SettingsIcon color="primary" sx={{ fontSize: 30, mr: 2 }} />
            <Typography variant="h4" component="h1">
              面试设置
            </Typography>
          </Box>

          <Divider sx={{ mb: 4 }} />

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel id="interview-type-label">面试职位</InputLabel>
                <Select
                  labelId="interview-type-label"
                  name="type"
                  value={formData.type}
                  onChange={handleChange}
                  label="面试职位"
                >
                  {Object.entries(interviewTypes).map(([key, value]) => (
                    <MenuItem key={key} value={key}>
                      {value}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="目标公司"
                name="company"
                value={formData.company}
                onChange={handleChange}
                placeholder="例如：阿里巴巴、腾讯、字节跳动等"
                helperText="可选，留空表示通用面试"
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel id="language-label">面试语言</InputLabel>
                <Select
                  labelId="language-label"
                  name="language"
                  value={formData.language}
                  onChange={handleChange}
                  label="面试语言"
                >
                  <MenuItem value="zh">中文</MenuItem>
                  <MenuItem value="en">英文</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Switch
                    checked={formData.useML}
                    onChange={handleChange}
                    name="useML"
                    color="primary"
                  />
                }
                label="启用机器学习优化"
              />
              <Typography variant="caption" color="text.secondary" display="block">
                系统将根据您的回答自动调整问题难度和方向
              </Typography>
            </Grid>
          </Grid>

          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Button
              variant="contained"
              size="large"
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <StartIcon />}
              onClick={handleStartInterview}
              disabled={loading}
              sx={{ py: 1.5, px: 4, fontSize: '1.1rem' }}
            >
              {loading ? '准备中...' : '开始面试'}
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Setup; 