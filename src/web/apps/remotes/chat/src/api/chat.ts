import { Http } from './http'

import  Config from '@/config';

const address = `${Config.value('API_GATEWAY_URL')}/api/v1/chat`;

export class ChatAPI {
    static async createTitle(title: string) {
        try {
          const res = await Http.post(
            `${address}/title`,
            {
              title: title,
            }
          );
          if (res.status !== 200) {
            throw new Error(`Response status is "${res.status}"`);
          }

          return res.data.data
        } catch (e) {
          console.error('createTitle error', e)
        } 
        return null;
    }

    static async updateTitle(id: string, title: string) {
        try {
          const res = await Http.patch(
            `${address}/title`,
            {
              id: id,
              title: title,
            }
          );
          if (res.status !== 200) {
            throw new Error(`Response status is "${res.status}"`);
          }

          return res.data.data
        } catch (e) {
          console.error('updateTitle error', e)
        } 
        return null;
    }

    static async deleteTitle(id: string) {
        try {
          const res = await Http.delete(
            `${address}/title`,
            {
              data: {
                id: id,
              }
            }
          );
          if (res.status !== 200) {
            throw new Error(`Response status is "${res.status}"`);
          }

          return res.data.data
        } catch (e) {
          console.error('deleteTitle error', e)
        } 
        return null;
    }

    static async createChat(parentId: string) {
        try {
          const res = await Http.post(
            `${address}`,
            {
              parent_id: parentId,
            }
          );
          if (res.status !== 200) {
            throw new Error(`Response status is "${res.status}"`);
          }

          return res.data.data
        } catch (e) {
          console.error('get error', e)
        } 
        return null;
    }

    static async getChat(chatId: string) {
        try {
          const res = await Http.get(
            `${address}?id=${chatId}`,
          );
          if (res.status !== 200) {
            throw new Error(`Response status is "${res.status}"`);
          }

          return res.data.data
        } catch (e) {
          console.error('get error', e)
        } 
        return null;
    }

    static async conversations(data: Object) {
        try {
          const res = await Http.post(
            `${address}/conversations`,
            data,
          );
          if (res.status !== 200) {
            throw new Error(`Response status is "${res.status}"`);
          }

          return res.data.data
        } catch (e) {
          console.error('get error', e)
        } 
        return null;
    }
}

