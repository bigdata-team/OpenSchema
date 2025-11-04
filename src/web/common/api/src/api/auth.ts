import { Http } from './http'
import { Config } from '@common/config';

const address = `${Config.value('API_GATEWAY_URL')}/api/v1/auth`;

export class AuthAPI {
    static async login() {
        try {
          const res = await Http.get(
            `${address}/login`,
	    {
		withCredentials: true
	    },
          );
          if (res.status !== 200) {
            throw new Error(`Response status is "${res.status}"`);
          }

          return res.data.data
        } catch (e) {
          console.error('login error', e)
        } 
        return null;
    }

    /*
    static async signinBySSO() {
        try {
          const res = await Http.get(
            `${address}/signin/sso`,
            {
              withCredentials: true,
            }
          );
          if (res.status !== 200) {
            throw new Error(`Response status is "${res.status}"`);
          }

          return res.data.data
        } catch (e) {
          console.error('me error', e)
        } 
        return null;
    }
    */

    static async refresh() {
        try {
          const res = await Http.get(
            `${address}/refresh`,
	    {
		withCredentials: true
	    },
          );
          if (res.status !== 200) {
            throw new Error(`Response status is "${res.status}"`);
          }

          return res.data.data
        } catch (e) {
          console.error('refresh error', e)
        } 
        return null;
    }
}
