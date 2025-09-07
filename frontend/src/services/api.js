import axios from 'axios'
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
export const fetchWeather = (lat, lon) => axios.get(`${API_URL}/weather`, { params: { lat, lon } }).then(r=>r.data)
export const recommendIrrigation = (lat, lon, talhao_id) => axios.get(`${API_URL}/recommendation/irrigation`, { params: { lat, lon, talhao_id } }).then(r=>r.data)
export const uploadPhoto = (file, talhao_id) => {
  const fd = new FormData();
  fd.append('file', file);
  fd.append('talhao_id', talhao_id);
  return axios.post(`${API_URL}/upload/photo`, fd, { headers: { 'Content-Type': 'multipart/form-data' } }).then(r=>r.data)
}
export const chat = (message, session_id) => {
  const fd = new FormData();
  fd.append('message', message);
  if(session_id) fd.append('session_id', session_id);
  return axios.post(`${API_URL}/chat`, fd).then(r=>r.data)
}
