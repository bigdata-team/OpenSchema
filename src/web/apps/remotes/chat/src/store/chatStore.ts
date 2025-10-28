import { create } from "zustand";

/**
 * CHAT STORE - UI State Management (Reactive)
 *
 * Purpose: Manages temporary, reactive UI state for real-time chat display
 * - Real-time message streaming
 * - Current user input
 * - Active conversation tracking
 * - Model selections
 *
 * Note: For persistent storage, see /model/chat.ts (chatHistory)
 */

export interface ChatMessage {
  role: "user" | "assistant";
  message: string;
}

type ChatState = {
  // Model management
  models: Record<string, string>; // chatContentID -> model mapping
  setModel: (chatContentID: string, model: string) => void;
  getModel: (chatContentID: string) => string | undefined;

  // Store messages for each chat instance by chatContentID and conversation index
  // Format: "conversationIndex:chatContentID" -> messages
  chats: Record<string, ChatMessage[]>;

  // Track streaming status for each chat
  isStreaming: Record<string, boolean>;

  // Current conversation index (increments with each new question)
  currentConversationIndex: number;

  // Current input message being typed
  currentInput: string;
  setCurrentInput: (message: string) => void;

  // Conversation history - stores user queries in order
  conversationHistory: string[];
  addConversation: (query: string) => void;

  // Initialize a chat with default messages
  initChat: (chatContentID: string, initialMessages: ChatMessage[]) => void;

  // Add an assistant message
  addAssistantMessage: (chatContentID: string, message: string) => void;

  // Update streaming message (for real-time updates)
  updateStreamingMessage: (chatContentID: string, delta: string, conversationIndex?: number) => void;

  // Start a new assistant message for streaming
  startStreaming: (chatContentID: string, conversationIndex?: number) => void;

  // Stop streaming
  stopStreaming: (chatContentID: string, conversationIndex?: number) => void;

  // Clear messages for a chat
  clearChat: (chatContentID: string) => void;

  // Get messages for a specific chat
  getMessages: (chatContentID: string) => ChatMessage[];
};

export const useChatStore = create<ChatState>((set, get) => ({
  // Model state
  models: {},

  setModel: (chatContentID: string, model: string) =>
    set((state) => ({
      models: { ...state.models, [chatContentID]: model },
    })),

  getModel: (chatContentID: string) => get().models[chatContentID],

  // Chat state
  chats: {},
  isStreaming: {},
  currentConversationIndex: 0,

  // Current input state
  currentInput: "",
  setCurrentInput: (message: string) => set({ currentInput: message }),

  // Conversation history state
  conversationHistory: [],
  addConversation: (query: string) =>
    set((state) => ({
      conversationHistory: [...state.conversationHistory, query],
      // Note: currentConversationIndex increments AFTER conversation completes
    })),

  initChat: (chatContentID: string, initialMessages: ChatMessage[]) =>
    set((state) => ({
      chats: { ...state.chats, [chatContentID]: initialMessages },
    })),

  addAssistantMessage: (chatContentID: string, message: string) =>
    set((state) => {
      const key = `${state.currentConversationIndex}:${chatContentID}`;
      const currentMessages = state.chats[key] || [];
      return {
        chats: {
          ...state.chats,
          [key]: [...currentMessages, { role: "assistant", message }],
        },
      };
    }),

  startStreaming: (chatContentID: string, conversationIndex?: number) =>
    set((state) => {
      const convIndex = conversationIndex !== undefined ? conversationIndex : state.currentConversationIndex;
      const key = `${convIndex}:${chatContentID}`;
      const currentMessages = state.chats[key] || [];
      return {
        chats: {
          ...state.chats,
          [key]: [...currentMessages, { role: "assistant", message: "" }],
        },
        isStreaming: {
          ...state.isStreaming,
          [key]: true,
        },
      };
    }),

  updateStreamingMessage: (chatContentID: string, delta: string, conversationIndex?: number) =>
    set((state) => {
      const convIndex = conversationIndex !== undefined ? conversationIndex : state.currentConversationIndex;
      const key = `${convIndex}:${chatContentID}`;
      const currentMessages = state.chats[key] || [];
      if (currentMessages.length === 0) return state;

      const lastMessageIndex = currentMessages.length - 1;
      const lastMessage = currentMessages[lastMessageIndex];

      if (lastMessage.role !== "assistant") return state;

      const updatedMessages = [...currentMessages];
      updatedMessages[lastMessageIndex] = {
        ...lastMessage,
        message: lastMessage.message + delta,
      };

      return {
        chats: {
          ...state.chats,
          [key]: updatedMessages,
        },
      };
    }),

  stopStreaming: (chatContentID: string, conversationIndex?: number) =>
    set((state) => {
      const convIndex = conversationIndex !== undefined ? conversationIndex : state.currentConversationIndex;
      const key = `${convIndex}:${chatContentID}`;
      return {
        isStreaming: {
          ...state.isStreaming,
          [key]: false,
        },
      };
    }),

  clearChat: (chatContentID: string) =>
    set((state) => {
      const key = `${state.currentConversationIndex}:${chatContentID}`;
      return {
        chats: {
          ...state.chats,
          [key]: [],
        },
      };
    }),

  getMessages: (chatContentID: string) => {
    const conversationIndex = get().currentConversationIndex;
    const key = `${conversationIndex}:${chatContentID}`;
    return get().chats[key] || [];
  },
}));

export default useChatStore;
