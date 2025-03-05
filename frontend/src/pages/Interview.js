import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  IconButton,
  CircularProgress,
  Alert,
  Divider,
  Card,
  CardContent,
  Chip,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions
} from '@mui/material';
import {
  Mic as MicIcon,
  MicOff as MicOffIcon,
  Send as SendIcon,
  VolumeUp as SpeakIcon,
  VolumeOff as MuteIcon,
  ExitToApp as ExitIcon,
  Help as HelpIcon
} from '@mui/icons-material';
// import axios from 'axios';

// 录音功能
const useRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      
      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };
      
      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
        setAudioBlob(blob);
        chunksRef.current = [];
      };
      
      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      console.error('无法访问麦克风:', err);
      alert('无法访问麦克风，请检查浏览器权限设置');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      // 停止所有音轨
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  return { isRecording, audioBlob, startRecording, stopRecording };
};

const Interview = () => {
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [answer, setAnswer] = useState('');
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [exitDialogOpen, setExitDialogOpen] = useState(false);
  const audioRef = useRef(null);
  
  // 录音功能
  const { isRecording, audioBlob, startRecording, stopRecording } = useRecorder();

  // 加载会话信息
  useEffect(() => {
    const sessionData = localStorage.getItem('interviewSession');
    if (!sessionData) {
      navigate('/setup');
      return;
    }
    
    try {
      const parsedSession = JSON.parse(sessionData);
      setSession(parsedSession);
      // 获取第一个问题
      fetchQuestion(parsedSession.interview_id);
    } catch (err) {
      console.error('解析会话数据失败:', err);
      navigate('/setup');
    }
  }, [navigate]);

  // 获取问题
  const fetchQuestion = async (interviewId) => {
    setLoading(true);
    setError('');

    try {
      const response = await api.get(`/api/interview/question?interview_id=${interviewId}`);
      
      if (response.data.status === 'success') {
        const question = response.data.data;
        setCurrentQuestion(question);
        setQuestions([...questions, question]);
        
        // 播放问题语音
        if (question.content) {
          playQuestionAudio(question.content);
        }
      } else {
        setError(response.data.message || '获取问题失败');
      }
    } catch (err) {
      console.error('获取问题请求失败:', err);
      setError('网络错误，请检查您的连接');
    } finally {
      setLoading(false);
    }
  };

  // 播放问题语音
  const playQuestionAudio = async (text) => {
    try {
      console.log("正在请求TTS API..."); const response = await api.post('/api/speech/tts', {
        text,
        language: session?.language || 'zh'
      });
      
      if (response.data.status === 'success') {
        const audioData = response.data.data.audio;
        const audioSrc = `data:audio/wav;base64,${audioData}`;
        
        if (audioRef.current) {
          audioRef.current.src = audioSrc;
          audioRef.current.play();
          setIsPlaying(true);
        }
      }
    } catch (err) {
      console.error('获取语音失败:', err);
    }
  };

  // 提交答案
  const submitAnswer = async () => {
    if (!answer.trim() || !currentQuestion || !session) return;
    
    setLoading(true);
    setError('');

    try {
      console.log("正在请求TTS API..."); const response = await api.post('/api/interview/answer', {
        interview_id: session.interview_id,
        question_id: currentQuestion.id,
        answer: answer
      });
      
      if (response.data.status === 'success') {
        const analysis = response.data.data;
        
        // 保存答案
        const newAnswer = {
          question: currentQuestion,
          content: answer,
          analysis
        };
        
        setAnswers([...answers, newAnswer]);
        setAnswer('');
        
        // 检查是否继续面试
        if (analysis.next_question) {
          // 获取下一个问题
          fetchQuestion(session.interview_id);
        } else {
          // 结束面试，导航到结果页面
          localStorage.setItem('interviewAnswers', JSON.stringify([...answers, newAnswer]));
          navigate('/results');
        }
      } else {
        setError(response.data.message || '提交答案失败');
      }
    } catch (err) {
      console.error('提交答案请求失败:', err);
      setError('网络错误，请检查您的连接');
    } finally {
      setLoading(false);
    }
  };

  // 语音识别
  const processAudioRecording = async () => {
    if (!audioBlob) return;
    
    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob);
      formData.append('language', session?.language || 'zh');
      
      console.log("正在请求TTS API..."); const response = await api.post('/api/speech/asr', formData);
      
      if (response.data.status === 'success') {
        const recognizedText = response.data.data.text;
        setAnswer(prev => prev + ' ' + recognizedText);
      }
    } catch (err) {
      console.error('语音识别失败:', err);
    } finally {
      setLoading(false);
    }
  };

  // 当录音停止时处理音频
  useEffect(() => {
    if (audioBlob && !isRecording) {
      processAudioRecording();
    }
  }, [audioBlob, isRecording]);

  // 音频播放结束事件
  useEffect(() => {
    const audioElement = audioRef.current;
    
    const handleEnded = () => {
      setIsPlaying(false);
    };
    
    if (audioElement) {
      audioElement.addEventListener('ended', handleEnded);
    }
    
    return () => {
      if (audioElement) {
        audioElement.removeEventListener('ended', handleEnded);
      }
    };
  }, []);

  // 退出面试
  const handleExit = () => {
    setExitDialogOpen(true);
  };

  const confirmExit = () => {
    localStorage.removeItem('interviewSession');
    navigate('/');
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h4" component="h1">
            AI面试模拟
          </Typography>
          <Tooltip title="退出面试">
            <IconButton color="error" onClick={handleExit}>
              <ExitIcon />
            </IconButton>
          </Tooltip>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              {session?.type && interviewTypes[session.type]} 面试
            </Typography>
            <Chip 
              label={session?.company || '通用公司'} 
              color="primary" 
              variant="outlined" 
            />
          </Box>
          
          <Divider sx={{ mb: 2 }} />
          
          <Box sx={{ minHeight: '100px', display: 'flex', alignItems: 'center' }}>
            {loading && !currentQuestion ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <CircularProgress />
              </Box>
            ) : currentQuestion ? (
              <Box>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Typography variant="subtitle1" color="text.secondary">
                    问题 {questions.length}:
                  </Typography>
                  <IconButton 
                    size="small" 
                    onClick={() => playQuestionAudio(currentQuestion.content)}
                    disabled={isPlaying}
                    sx={{ ml: 1 }}
                  >
                    {isPlaying ? <MuteIcon fontSize="small" /> : <SpeakIcon fontSize="small" />}
                  </IconButton>
                </Box>
                <Typography variant="h6">{currentQuestion.content}</Typography>
              </Box>
            ) : (
              <Typography variant="body1" color="text.secondary">
                准备开始面试...
              </Typography>
            )}
          </Box>
        </Paper>

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="subtitle1" gutterBottom>
              您的回答:
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={6}
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="在此输入您的回答..."
              disabled={loading || !currentQuestion}
              sx={{ mb: 2 }}
            />
            
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
              <Box>
                <Tooltip title={isRecording ? "停止录音" : "开始语音输入"}>
                  <IconButton 
                    color={isRecording ? "error" : "primary"}
                    onClick={isRecording ? stopRecording : startRecording}
                    disabled={loading || !currentQuestion}
                  >
                    {isRecording ? <MicOffIcon /> : <MicIcon />}
                  </IconButton>
                </Tooltip>
                {isRecording && (
                  <Typography variant="caption" color="error" component="span" sx={{ ml: 1 }}>
                    正在录音...
                  </Typography>
                )}
              </Box>
              
              <Button
                variant="contained"
                endIcon={<SendIcon />}
                onClick={submitAnswer}
                disabled={loading || !answer.trim() || !currentQuestion}
              >
                {loading ? '提交中...' : '提交回答'}
              </Button>
            </Box>
          </CardContent>
        </Card>

        {answers.length > 0 && (
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              已回答问题:
            </Typography>
            <Box sx={{ maxHeight: '200px', overflowY: 'auto' }}>
              {answers.map((item, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    问题 {index + 1}: {item.question.content}
                  </Typography>
                  <Typography variant="body2" sx={{ ml: 2 }}>
                    {item.content}
                  </Typography>
                  <Divider sx={{ my: 1 }} />
                </Box>
              ))}
            </Box>
          </Paper>
        )}
      </Box>

      {/* 音频元素 */}
      <audio ref={audioRef} style={{ display: 'none' }} />

      {/* 退出确认对话框 */}
      <Dialog
        open={exitDialogOpen}
        onClose={() => setExitDialogOpen(false)}
      >
        <DialogTitle>确认退出面试?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            退出后，当前面试进度将丢失。您确定要退出吗？
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setExitDialogOpen(false)}>取消</Button>
          <Button onClick={confirmExit} color="error">
            确认退出
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

// 面试类型映射
const interviewTypes = {
  'software_engineer': '软件工程师',
  'product_manager': '产品经理',
  'data_scientist': '数据科学家',
  'frontend_developer': '前端开发工程师',
  'backend_developer': '后端开发工程师'
};

export default Interview; 