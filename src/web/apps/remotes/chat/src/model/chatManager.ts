import { ChatAPI } from "@common/api";
import { Chat } from './chat';
import { useNotificationStore } from '@/store/notificationStore';
import { modelManager } from "./modelManager";

class ChatManager {
    private titles: Array<Chat> = [];
    // private processing: Promise<boolean> = Promise.resolve(false);
    private processing: boolean = false;
    private initPromise: Promise<boolean>;

    constructor() {
      this.initPromise = this._initialize();
    }

    public async waitForInitialization(): Promise<boolean> {
      return await this.initPromise;
    }

    private async _initialize(): Promise<boolean> {
        console.log("ChatManager initializing...");
        // for initialize of modelManager
        modelManager;
       
        const list = await ChatAPI.listTitle();
        if (list) {
            for (const t of list) {
                // console.log("Title:", t.id, t.title);
                const title = new Chat(t);
                this.titles.push(title);
            }
        }
        console.log("ChatManager initialized with titles:", this.titles);
        useNotificationStore.getState().notifyTitlesChanged();
        return true;
    }

    async createNewTitle(titleText: string): Promise<Chat | null> {
        await this.waitForInitialization();

        const newTitleData = await ChatAPI.createTitle(titleText);
        if (newTitleData) {
            const newTitle = new Chat(newTitleData);
            this.titles.unshift(newTitle);
            useNotificationStore.getState().notifyTitlesChanged();
            return newTitle;
        }
        return null;
    }

    async getTitles() {
        // TODO
        await this.waitForInitialization();
        return this.titles;
    }

    // TODO name fetchChildrenForTitle
    async fetchChildrenForTitle(titleId: string) {
        // TODO
        await this.waitForInitialization();

        if (this.processing) {
            console.warn("ChatManager is already processing. Please wait.");
            return null;
        }
        this.processing = true;

        if (!titleId || titleId.length === 0) return;
        const title = this.titles.find(t => t.id === titleId);
        if (!title) {
            console.warn("Title not found:", titleId);
            return null;
        }

        const titleWithChildren = await ChatAPI.getChat(title.id);
        // console.log("Fetched chat for title:", title.id, titleWithChildren);
        if (!titleWithChildren || !titleWithChildren.children) return;
        // console.log(" - children:", titleWithChildren.children.length);

        const oldeTitleChildren = title.children;
        title.children = []; // clear existing children
        for (const child1 of titleWithChildren.children) {
            const oldChat = oldeTitleChildren.find(c => c.id === child1.id);
            // console.log(" -- titleWithChildren:", child1.id, child1.children.length, oldChat?.children.length);
            const newChat = new Chat(child1);
            if (oldChat && oldChat.children.length > 0 && newChat.children.length < oldChat.children.length) {
                newChat.children = oldChat.children;
            }
            title.addChild(newChat);
        }

        console.log("Finished fetching children for title:", title);
        this.processing = false;
        return title;
    }

    async getTitleById(titleId: string): Promise<Chat | null> {
        // TODO
        await this.waitForInitialization();

        if (!titleId) return null;
        return this.titles.find(t => t.id === titleId) || null;
    }

    async addChildByTitileId(titleId: string, child: Chat): Promise<void> {
        // TODO
        await this.waitForInitialization();

        const title = this.titles.find(t => t.id === titleId);
        if (!title) {
            console.warn("Title not found:", titleId);
            return;
        }
        title.addChild(child);
    }

    async getChildrenByTitleId(titleId: string): Promise<Array<Chat>> {
        // TODO
        await this.waitForInitialization();

        const title = this.titles.find(t => t.id === titleId);
        if (!title) {
            console.warn("Title not found:", titleId);
            return [];
        }
        return title.children; 
    }

    // TODO do not need
    async getChatByIndex(id: string, conversationIndex: number|undefined, modelIndex: number): Promise<Chat | null> {
        // TODO
        await this.waitForInitialization();

        if (conversationIndex === undefined) {
            console.log('getChatByIndex: conversationIndex is undefined');
            return null;
        }

        const title = await this.getTitleById(id);
        if (!title) {
            console.log('getChatByIndex: title not found for id:', id);
            return null;
        }

        // console.log('getChatByIndex: title.children.length:', title.children.length, 'conversationIndex:', conversationIndex);
        if (title.children.length <= conversationIndex) {
            console.log('getChatByIndex: conversationIndex out of bounds');
            return null;
        }

        const child1 = title.children[conversationIndex];
        // console.log('getChatByIndex: child1:', child1.id, 'child1.children.length:', child1.children.length, 'modelIndex:', modelIndex);
        if (child1.children.length <= modelIndex) {
            console.log('getChatByIndex: modelIndex out of bounds, returning child1 instead');
            // If there are no children, return the parent conversation itself
            // return child1;
            return null;
        }

        return child1.children[modelIndex];
    }

    async getChatById(titleId: string, chatId: string): Promise<Chat | null> {
        // TODO
        await this.waitForInitialization();

        const title = await this.getTitleById(titleId);
        if (!title) {
            console.log('getChatById: title not found for titleId:', titleId);
            return null;
        }

        const chat = title.children.find(c => c.id === chatId);
        // console.log('getChatById: child1:', child1.id, 'child1.children.length:', child1.children.length, 'modelIndex:', modelIndex);
        if (!chat) {
            console.log('getChatById: modelIndex out of bounds, returning null', titleId, chatId);
            return null;
        }

        return chat;
    }
}


export const chatManager = new ChatManager();
