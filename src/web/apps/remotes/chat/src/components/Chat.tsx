import ReactMarkdown from "react-markdown";
import "@/index.css";

export interface Chatting {
    model: string;
    message: Array<{
        role: string;
        message: string;
    }>;
}

export let chatting: Chatting = {
    model: "gpt-4o",
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
};

export default function Chat({
    chatContentID,
}: {
    chatContentID: string;
}) {
    return (
        <div>
            <div className="bg-surface-primary relative flex w-full min-w-100 flex-1 flex-col overflow-hidden transition-all duration-300 rounded-2xl border border-border-faint">
                <div className="bg-surface-primary border-border-faint/50 sticky top-0 flex w-full flex-none items-center justify-between gap-2 h-[40px] px-3 py-2">
                    <div className="pointer-events-none absolute right-2 top-2 flex size-6 items-center justify-center" data-sentry-component="VoteHoverIcon" data-sentry-source-file="vote-hover-icon.tsx">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
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
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
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
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            className="lucide lucide-thumbs-down absolute opacity-0 transition-opacity duration-300"
                            data-sentry-element="ThumbsDown"
                            data-sentry-source-file="vote-hover-icon.tsx"
                        >
                            <path d="M17 14V2"></path>
                            <path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22a3.13 3.13 0 0 1-3-3.88Z"></path>
                        </svg>
                    </div>
                    <div className="flex min-w-0 flex-1 items-center gap-2">
                        <span className="xs:max-w-full flex min-w-0 max-w-[250px] items-center gap-1 font-mono text-xs font-medium">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" height="24" width="24" className="mr-2 flex-shrink-0 size-3.5">
                                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"></path>
                                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"></path>
                                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"></path>
                                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"></path>
                                <path d="M1 1h22v22H1z" fill="none"></path>
                            </svg>
                            <span className="truncate">{chatting.model}</span>
                        </span>
                    </div>
                    <div className="text-text-primary flex items-center gap-2 transition-opacity duration-300 opacity-100" data-sentry-component="MessageActions" data-sentry-source-file="message-header.tsx">
                        <button
                            className="inline-flex items-center justify-center gap-2 whitespace-nowrap transition-colors focus-visible:ring-2 focus-visible:ring-ring ring-offset-2 focus-visible:ring-offset-surface-primary disabled:pointer-events-none disabled:opacity-50 [&amp;_svg]:pointer-events-none [&amp;_svg]:shrink-0 text-sm font-medium hover:bg-surface-tertiary hover:text-accent-foreground focus-visible:outline-none focus-visible:border-none size-3 rounded-md p-3"
                            type="button"
                            data-state="closed"
                            data-sentry-element="TooltipTrigger"
                            data-sentry-source-file="basic-tooltip.tsx"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-refresh-cw">
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
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
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
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
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
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-maximize2">
                                <polyline points="15 3 21 3 21 9"></polyline>
                                <polyline points="9 21 3 21 3 15"></polyline>
                                <line x1="21" x2="14" y1="3" y2="10"></line>
                                <line x1="3" x2="10" y1="21" y2="14"></line>
                            </svg>
                        </button>
                    </div>
                </div>
                <div className="no-scrollbar relative flex w-full flex-1 flex-col overflow-x-auto transition-[max-height] duration-300 max-h-[max(50svh,350px)] overflow-y-auto border-border-faint border-t">
                    {chatting.message.map(chat => { if (chat.role == "assistant") return (
                    <div className="min-w-0 p-3">
                        <div id={chatContentID} className="prose prose-sm prose-pre:bg-transparent prose-pre:p-0 text-wrap break-words">
                            <ReactMarkdown>
                                {chat.message}
                            </ReactMarkdown>
                        </div>
                    </div>
                    ); else return (
                    <div className="min-w-0 p-3">
                        <div id={chatContentID} className="prose prose-sm prose-pre:bg-transparent prose-pre:p-0 text-wrap break-words">
                            {chat.message}
                        </div>
                    </div>
                    ); })}
                </div>
            </div>
        </div>

    );
}   