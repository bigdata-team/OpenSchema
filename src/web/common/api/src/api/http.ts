import axios  from 'axios'
import { user } from '../user';

export const Http = axios.create({
});
  

Http.interceptors.request.use(
  async(request:any) => {
    console.log('TODO >>> http.js request:', request.url)
    if (request.url.includes('/signup') || request.url.includes('/signin') || request.url.includes('/refresh')
    ) {
      // no token: do nothing
    } else if (!user.isTokenValid()) {
      console.log('TODO >>> http.js', request.url)
      const valid = await user.refresh()
      if (!valid) {
        // TODO logout
        // TODO move to login page
        // router.push({ name: 'Login' }).catch(() => {})
        const err = new Error('Token expired')
        return Promise.reject(err)
      }

      const accessToken = user.getToken()
      request.headers.Authorization = `Bearer ${accessToken}`
    } else {
      const accessToken = user.getToken()
      request.headers.Authorization = `Bearer ${accessToken}`
    }

    return request;
  }
);
