import axios from "axios";

// 设置API基础URL
// 开发环境使用相对路径，生产环境使用环境变量中的URL或默认URL
const API_BASE_URL = process.env.NODE_ENV === "production"
  ? (process.env.REACT_APP_API_URL || window.location.origin)
  : "";

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log(`发送请求到: ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error("API请求错误:", error);
    if (error.response) {
      console.error("错误响应数据:", error.response.data);
    }
    return Promise.reject(error);
  }
);

export default api;
