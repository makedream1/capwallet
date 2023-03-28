import axios from 'axios';

const HOST = 'https://volreviews.com'

export const BASE_URL = `${HOST}/api/v1`;


export const fetchDataApi = (user_id: string) => {
  return axios.get(`${BASE_URL}/users/${user_id}`)
    .then(function (response) {
      return response.data;
    })
    .catch(function (error) {
      console.error(error);
    });
};
