import axios from 'axios';

const HOST = 'https://volreviews.com'

export const BASE_URL = `${HOST}/api/v1`;


export const fetchDataApi = async (user_id: string): Promise<{ data: {} }> => {
  const response = await axios.get(`${BASE_URL}/users/${user_id}`);
  return response.data;
};
