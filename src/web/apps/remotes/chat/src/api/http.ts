import axios  from 'axios'
import  Config from '@/config';

export const Http = axios.create({
});
  

Http.interceptors.request.use(
  async(request:any) => {
    if (request.url.includes('/signup') || request.url.includes('/signin') || request.url.includes('/refresh')
    ) {
      // no token: do nothing
    } else {
      request.headers.Authorization = `Bearer ${Config.value("TEMP_ACCESS_TOKEN")}`;
    }

    return request;
  }
);
