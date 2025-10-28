import { Http } from './http'

import  Config from '@/config';

const address = `${Config.value('API_GATEWAY_URL')}/api/v1/chat`;

export class ChatAPI {
    static async get(chatId: string) {
        try {
          const res = await Http.get(
            `${address}?id=${chatId}`,
          );
          console.log('ChatAPI.get response:', res);
          if (res.status !== 200) {
            throw new Error(`Response status is "${res.status}"`);
          }

          return res.data.data
        } catch (e) {
          console.error('count error', e)
        } 
        return null;
    }
}

