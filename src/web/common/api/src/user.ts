
import { jwtDecode, type JwtPayload } from 'jwt-decode'
import { AuthAPI } from './api/auth'
import { LocalStorage } from '@common/util';
// import { Config } from '@common/config';

class User {
    uID: string | undefined = undefined;
    accessToken: string | null = null;
    ready: false | true = false;

    constructor() {
      // TODO temp code
      this.accessToken = LocalStorage.getItem('accessToken')
      // TODO temp code
      // this.accessToken = Config.value("TEMP_ACCESS_TOKEN");
    } 

    isTokenValid() {
      if (!this.accessToken) {
        console.log('TODO >>> isTokenValid > no accessToken')
        return false
      }

      const token: JwtPayload = jwtDecode(this.accessToken)
      if (!token.exp || token.exp <= Date.now() / 1000) {
        console.log('TODO >>> token expired <<<')
        return false
      }

      return true
    }

    async refresh(forcibly = false) {
      console.log('TODO >>> User.refresh', forcibly)
      if (!forcibly && this.isTokenValid()) {
        this.ready = true
        return true
      }
      const uID = LocalStorage.getItem('uID')
      if (!uID) {
        console.log('TODO >>> User.refresh > no login')
        this.ready = true
        return false
      }
      try {
        const result = await AuthAPI.refresh()
        if (!result || !result.access_token) {
          console.log('refresh fail')
          this.ready = true
          return false
        }
        this.setToken(result.access_token)
        this.ready = true
        return true
      } catch (e) {
        console.error('refresh error:', e)
        // TODO logout
        alert('Your login has expired.\nPlease log in again.')
        this.ready = true
        return false
      }
    }

    login(accessToken: string) {
      this.setToken(accessToken)
    }

    getToken() {
      return this.accessToken
    }

    setToken(accessToken: string) {
      this.accessToken = accessToken
      // TODO temp code
      LocalStorage.setItem('accessToken', accessToken)

      if (this.accessToken) {
        const token = jwtDecode(this.accessToken)
        this.uID = token.sub
        LocalStorage.setItem('uID', this.uID)
      } else {
        this.uID = undefined
        LocalStorage.removeItem('uID')
      }
    }
}

export const user = new User();
