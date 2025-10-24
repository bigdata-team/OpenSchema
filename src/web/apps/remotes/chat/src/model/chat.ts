/**
 * CHAT MODELS & PERSISTENT DATA
 *
 * Purpose: Define data models and persistent storage
 * - Model definitions (GPT, Gemini, Claude)
 * - Chat history for persistence/database
 * - Helper functions for data operations
 *
 * Note: For reactive UI state, see /store/chatStore.ts
 */

export interface Chatting {
    name: string;
    model: string;
    message: Array<{
        role: "user" | "assistant";
        message: string;
    }>;
}

export const chatting: Chatting[] = [
    {
        name: "gpt-5-pro",
        // TODO model: "openai/gpt-5-pro",
        model: "openai/gpt-5",
        message: [
            {
                role:"user",
                message:"hello"
            },
            {
                role:"assistant",
                message:"nice to meet you"
            },
        ]
    },
    {
        name: "gemini-2.5-pro",
        // TODO model: "google/gemini-2.5-pro",
        model: "google/gemini-2.5-flash",
        message: [
            {
                role:"user",
                message:"hello"
            },
            {
                role:"assistant",
                message:"nice to meet you"
            },
        ]
    },
    {
        name: "claude-sonnet-4.5",
        model: "anthropic/claude-sonnet-4.5",
        message: [
            {
                role:"user",
                message:"hello"
            },
            {
                role:"assistant",
                message:"nice to meet you"
            },
        ]
    }
];

// Interface for storing conversation history
export interface ChatHistory {
    userQuestion: string;
    timestamp: Date;
    responses: {
        [chatId: string]: {
            modelName: string;
            model: string;
            message: string;
        };
    };
}

export const chatHistory: ChatHistory[] = [];

// Helper function to add conversation to history
export function addToChatHistory(
    userQuestion: string,
    responses: { [chatId: string]: { modelName: string; model: string; message: string } }
) {
    chatHistory.push({
        userQuestion,
        timestamp: new Date(),
        responses,
    });
}

// Helper function to update a response in the latest conversation
export function updateLatestResponse(chatId: string, modelName: string, model: string, message: string) {
    if (chatHistory.length > 0) {
        const latest = chatHistory[chatHistory.length - 1];
        if (!latest.responses[chatId]) {
            latest.responses[chatId] = { modelName, model, message: "" };
        }
        latest.responses[chatId].message += message;
    }
}