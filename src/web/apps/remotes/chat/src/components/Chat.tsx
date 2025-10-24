import ReactMarkdown from "react-markdown";
import "@/index.css";
import React from "react";
import { useChatStore } from "@/store";
import { chatting } from "@/model/chat";

export default function Chat({
    chatContentID,
    conversationIndex,
}: {
    chatContentID: string;
    conversationIndex?: number;
}) {
    // Map chatContentID to index: "abcd" -> 0, "bcde" -> 1, "efgh" -> 2
    const chatIndex = chatContentID === "abcd" ? 0 : chatContentID === "bcde" ? 1 : 2;

    // Get Zustand store functions (now all from useChatStore)
    const { models, setModel, chats, initChat, currentConversationIndex } = useChatStore();

    // Use provided conversationIndex or current one
    const convIndex = conversationIndex !== undefined ? conversationIndex : currentConversationIndex;

    // Initialize model and chat messages in store on mount
    React.useEffect(() => {
        if (!models[chatContentID]) {
            setModel(chatContentID, chatting[chatIndex].model);
        }
        // Initialize chat with default messages if not already initialized
        if (!chats[chatContentID]) {
            initChat(chatContentID, chatting[chatIndex].message);
        }
    }, [chatContentID, chatIndex, models, setModel, chats, initChat]);

    // Get current chat based on default chatIndex
    const currentChat = chatting[chatIndex];

    // Get messages from store for this specific conversation (this will update reactively)
    const chatKey = `${convIndex}:${chatContentID}`;
    const messages = chats[chatKey] || currentChat.message;

    // Get the currently selected model from the store
    const selectedModelId = models[chatContentID] || chatting[chatIndex].model;
    // Find the model name from the chatting array
    const selectedModelName = chatting.find(chat => chat.model === selectedModelId)?.name || chatting[chatIndex].name;

    return (
        <div className="w-full">
            <div className="bg-surface-primary relative flex w-full flex-1 flex-col overflow-hidden transition-all duration-300 rounded-2xl border border-border-faint">
                <div className="bg-surface-primary border-border-faint/50 sticky top-0 flex w-full flex-none items-center justify-between gap-2 h-[40px] px-3 py-2">
                    <div className="pointer-events-none absolute right-2 top-2 flex size-6 items-center justify-center" data-sentry-component="VoteHoverIcon" data-sentry-source-file="vote-hover-icon.tsx">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            className="lucide lucide-handshake absolute opacity-0 transition-opacity duration-300"
                            data-sentry-element="Handshake"
                            data-sentry-source-file="vote-hover-icon.tsx"
                        >
                            <path d="m11 17 2 2a1 1 0 1 0 3-3"></path>
                            <path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"></path>
                            <path d="m21 3 1 11h-2"></path>
                            <path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"></path>
                            <path d="M3 4h8"></path>
                        </svg>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            className="lucide lucide-trophy absolute opacity-0 transition-opacity duration-300"
                            data-sentry-element="Trophy"
                            data-sentry-source-file="vote-hover-icon.tsx"
                        >
                            <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path>
                            <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path>
                            <path d="M4 22h16"></path>
                            <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path>
                            <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path>
                            <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path>
                        </svg>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            className="lucide lucide-thumbs-down absolute opacity-0 transition-opacity duration-300"
                            data-sentry-element="ThumbsDown"
                            data-sentry-source-file="vote-hover-icon.tsx"
                        >
                            <path d="M17 14V2"></path>
                            <path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22a3.13 3.13 0 0 1-3-3.88Z"></path>
                        </svg>
                    </div>
                    <div className="flex min-w-0 flex-1 items-center gap-2">
                        <div className="flex items-center gap-2">
                            {selectedModelName === "gpt-5-pro" && (
                                <svg xmlns="http://www.w3.org/2000/svg" strokeLinejoin="round" viewBox="0 0 16 16" height="24" width="24" className="w-4 h-4">
                                    <path d="M14.9449 6.54871C15.3128 5.45919 15.1861 4.26567 14.5978 3.27464C13.7131 1.75461 11.9345 0.972595 10.1974 1.3406C9.42464 0.481584 8.3144 -0.00692594 7.15045 7.42132e-05C5.37487 -0.00392587 3.79946 1.1241 3.2532 2.79113C2.11256 3.02164 1.12799 3.72615 0.551837 4.72468C-0.339497 6.24071 -0.1363 8.15175 1.05451 9.45178C0.686626 10.5413 0.813308 11.7348 1.40162 12.7258C2.28637 14.2459 4.06498 15.0279 5.80204 14.6599C6.5743 15.5189 7.68504 16.0074 8.849 15.9999C10.6256 16.0044 12.2015 14.8754 12.7478 13.2069C13.8884 12.9764 14.873 12.2718 15.4491 11.2733C16.3394 9.75728 16.1357 7.84774 14.9454 6.54771L14.9449 6.54871ZM8.85001 14.9544C8.13907 14.9554 7.45043 14.7099 6.90468 14.2604C6.92951 14.2474 6.97259 14.2239 7.00046 14.2069L10.2293 12.3668C10.3945 12.2743 10.4959 12.1008 10.4949 11.9133V7.42173L11.8595 8.19925C11.8742 8.20625 11.8838 8.22025 11.8858 8.23625V11.9558C11.8838 13.6099 10.5263 14.9509 8.85001 14.9544ZM2.32133 12.2028C1.9651 11.5958 1.8369 10.8843 1.95902 10.1938C1.98284 10.2078 2.02489 10.2333 2.05479 10.2503L5.28366 12.0903C5.44733 12.1848 5.65003 12.1848 5.81421 12.0903L9.75604 9.84429V11.3993C9.75705 11.4153 9.74945 11.4308 9.73678 11.4408L6.47295 13.3004C5.01915 14.1264 3.1625 13.6354 2.32184 12.2028H2.32133ZM1.47155 5.24819C1.82626 4.64017 2.38619 4.17516 3.05305 3.93366C3.05305 3.96116 3.05152 4.00966 3.05152 4.04366V7.72424C3.05051 7.91124 3.15186 8.08475 3.31654 8.17725L7.25838 10.4228L5.89376 11.2003C5.88008 11.2093 5.86285 11.2108 5.84765 11.2043L2.58331 9.34327C1.13255 8.51426 0.63494 6.68272 1.47104 5.24869L1.47155 5.24819ZM12.6834 7.82274L8.74157 5.57669L10.1062 4.79968C10.1199 4.79068 10.1371 4.78918 10.1523 4.79568L13.4166 6.65522C14.8699 7.48373 15.3681 9.31827 14.5284 10.7523C14.1732 11.3593 13.6138 11.8243 12.9474 12.0663V8.27575C12.9489 8.08875 12.8481 7.91574 12.6839 7.82274H12.6834ZM14.0414 5.8057C14.0176 5.7912 13.9756 5.7662 13.9457 5.7492L10.7168 3.90916C10.5531 3.81466 10.3504 3.81466 10.1863 3.90916L6.24442 6.15521V4.60017C6.2434 4.58417 6.251 4.56867 6.26367 4.55867L9.52751 2.70063C10.9813 1.87311 12.84 2.36563 13.6781 3.80066C14.0323 4.40667 14.1605 5.11618 14.0404 5.8057H14.0414ZM5.50257 8.57726L4.13744 7.79974C4.12275 7.79274 4.11312 7.77874 4.11109 7.76274V4.04316C4.11211 2.38713 5.47368 1.0451 7.15197 1.0461C7.86189 1.0461 8.54902 1.2921 9.09476 1.74011C9.06993 1.75311 9.02737 1.77661 8.99899 1.79361L5.77012 3.63365C5.60493 3.72615 5.50358 3.89916 5.50459 4.08666L5.50257 8.57626V8.57726ZM6.24391 7.00022L7.99972 5.9997L9.75553 6.99972V9.00027L7.99972 10.0003L6.24391 9.00027V7.00022Z"></path>
                                </svg>
                            )}
                            {selectedModelName === "gemini-2.5-pro" && (
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" height="24" width="24" className="w-4 h-4">
                                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"></path>
                                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"></path>
                                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"></path>
                                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"></path>
                                    <path d="M1 1h22v22H1z" fill="none"></path>
                                </svg>
                            )}
                            {selectedModelName === "claude-sonnet-4.5" && (
                                <svg fill="currentColor" fillRule="evenodd" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg" className="w-4 h-4">
                                    <title>Anthropic</title>
                                    <path d="M13.827 3.52h3.603L24 20h-3.603l-6.57-16.48zm-7.258 0h3.767L16.906 20h-3.674l-1.343-3.461H5.017l-1.344 3.46H0L6.57 3.522zm4.132 9.959L8.453 7.687 6.205 13.48H10.7z"></path>
                                </svg>
                            )}
                            <span className="text-xs font-medium font-mono">{selectedModelName}</span>
                        </div>
                    </div>
                    <div className="text-text-primary flex items-center gap-2 transition-opacity duration-300 opacity-100" data-sentry-component="MessageActions" data-sentry-source-file="message-header.tsx">
                        <button
                            className="inline-flex items-center justify-center gap-2 whitespace-nowrap transition-colors focus-visible:ring-2 focus-visible:ring-ring ring-offset-2 focus-visible:ring-offset-surface-primary disabled:pointer-events-none disabled:opacity-50 [&amp;_svg]:pointer-events-none [&amp;_svg]:shrink-0 text-sm font-medium hover:bg-surface-tertiary hover:text-accent-foreground focus-visible:outline-none focus-visible:border-none size-3 rounded-md p-3"
                            type="button"
                            data-state="closed"
                            data-sentry-element="TooltipTrigger"
                            data-sentry-source-file="basic-tooltip.tsx"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-refresh-cw">
                                <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"></path>
                                <path d="M21 3v5h-5"></path>
                                <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"></path>
                                <path d="M8 16H3v5"></path>
                            </svg>
                        </button>
                        <button
                            className="inline-flex items-center justify-center gap-2 whitespace-nowrap transition-colors focus-visible:ring-2 focus-visible:ring-ring ring-offset-2 focus-visible:ring-offset-surface-primary disabled:pointer-events-none disabled:opacity-50 [&amp;_svg]:pointer-events-none [&amp;_svg]:shrink-0 text-sm font-medium hover:bg-surface-tertiary hover:text-accent-foreground focus-visible:outline-none focus-visible:border-none relative size-3 rounded-md p-3"
                            type="button"
                            data-state="closed"
                            data-sentry-element="Button"
                            data-sentry-source-file="copy-button.tsx"
                            data-sentry-component="CopyButton"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="14"
                                height="14"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                className="lucide lucide-check text-interactive-positive absolute left-1.5 top-1.5 rotate-90 opacity-0 transition-all duration-300"
                                data-sentry-element="Check"
                                data-sentry-source-file="copy-button.tsx"
                            >
                                <path d="M20 6 9 17l-5-5"></path>
                            </svg>
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="14"
                                height="14"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                className="lucide lucide-copy opacity-100 transition-opacity duration-300"
                                data-sentry-element="Copy"
                                data-sentry-source-file="copy-button.tsx"
                            >
                                <rect width="14" height="14" x="8" y="8" rx="2" ry="2"></rect>
                                <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"></path>
                            </svg>
                        </button>
                        <button
                            className="inline-flex items-center justify-center gap-2 whitespace-nowrap transition-colors focus-visible:ring-2 focus-visible:ring-ring ring-offset-2 focus-visible:ring-offset-surface-primary disabled:pointer-events-none disabled:opacity-50 [&amp;_svg]:pointer-events-none [&amp;_svg]:shrink-0 text-sm font-medium hover:bg-surface-tertiary hover:text-accent-foreground focus-visible:outline-none focus-visible:border-none size-3 rounded-md p-3"
                            type="button"
                            data-state="closed"
                            data-sentry-element="TooltipTrigger"
                            data-sentry-source-file="basic-tooltip.tsx"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-maximize2">
                                <polyline points="15 3 21 3 21 9"></polyline>
                                <polyline points="9 21 3 21 3 15"></polyline>
                                <line x1="21" x2="14" y1="3" y2="10"></line>
                                <line x1="3" x2="10" y1="21" y2="14"></line>
                            </svg>
                        </button>
                    </div>
                </div>
                <div className="no-scrollbar relative flex w-full flex-1 flex-col overflow-x-auto transition-[max-height] duration-300 max-h-[max(50svh,350px)] overflow-y-auto border-border-faint border-t">
                    {messages.map((chat, index) => { if (chat.role == "assistant") return (
                    <div key={index} className="min-w-0 p-3">
                        <div className="prose prose-sm prose-pre:bg-transparent prose-pre:p-0 text-wrap break-words">
                            <ReactMarkdown>
                                {chat.message}
                            </ReactMarkdown>
                        </div>
                    </div>
                    ); else return (
                    <div key={index} className="min-w-0 p-3">
                        <div className="prose prose-sm prose-pre:bg-transparent prose-pre:p-0 text-wrap break-words">
                            {chat.message}
                        </div>
                    </div>
                    ); })}
                </div>
            </div>
        </div>

    );
}   