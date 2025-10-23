import React from 'react';
import type { ChangeEvent, KeyboardEvent } from "react";
import  Config from '@/config';
import "@/index.css";


export async function processChat(str: string,targetID:string) {

    let targetDiv = document.getElementById(targetID);
    if(!targetDiv)
        return "error";

    // const url = `https://api.openai.com/v1/chat/completions`
    const url = `${Config.value("API_GATEWAY_URL")}/api/v1/chat/completions`;
    const response = await fetch(url, {
        method: `POST`,
        headers: {
            "content-type": `application/json`,
            Authorization: `Bearer ${Config.value("TEMP_ACCESS_TOKEN")}`,
        },
        body: JSON.stringify({
            model:"openai/gpt-4o",
            messages:[
                {
                    role:"user",
                    content:str
                }
            ],
            stream:true
        }),
    });

    const reader = response.body?.getReader();
    if(!reader)
    {
        targetDiv.textContent = `error at ${targetID} #1`;
        return "error";
    }
    const decoder = new TextDecoder("utf-8");
    let responseChat = "";
    let buffer = "";

    while (true) {
        const { done, value } = await reader.read();

        if (done) {
            break;
        }

        buffer += decoder.decode(value, { stream: true });

        // 줄 단위로 분리
        const lines = buffer.split("\n");
        buffer = lines.pop() || ""; // 마지막 줄은 아직 덜 들어온 데이터일 수 있음

        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed.startsWith("data:")) continue;
            const data = trimmed.replace(/^data:\s*/, "");

            if (data === "[DONE]") {
                console.log("\n✅ 스트리밍 완료!");
                break;
            }

            try {
                const json = JSON.parse(data);
                const delta = json.choices?.[0]?.delta?.content;
                if (delta) {
                    // 부분 출력
                    console.log(delta);
                    responseChat += delta;
                    //process.stdout.write(delta);
                }
            } catch (err) {
                responseChat += `error at ${targetID} #2`;
            }
        }
        
        //responseChat += chunk;

        targetDiv.textContent = responseChat;
    }

    if(responseChat == "")
        targetDiv.textContent = `no response at ${targetID}`;

    //console.log(responseChat);
    return responseChat;
}

export default function SendChat({
    targetID
}:{
    targetID:Array<string>;
})
{

    HTMLTextAreaElement;
    let [message,setMessage] = React.useState("");
    const handleMessageInput = (e:ChangeEvent<HTMLTextAreaElement>) => {
        setMessage(e.target.value);
    }

    async function processKeyboardInput(event:KeyboardEvent)
    {
        console.log(event);
        if(event.key == "Enter" && event.shiftKey == false)
        {
            let promiseList = targetID.map((id) => {return processChat(message,id);});
            await Promise.all(promiseList);

            setMessage("");
            event.preventDefault();
        }
    }

    return (
        <div className="border-border-faint bg-surface-primary relative mx-auto min-h-0 w-full flex-none rounded-[14px] border">
            <form className="flex w-full flex-col items-start justify-center p-2">
            <div className="flex w-full flex-col justify-between gap-1 md:gap-2">
                <input
                accept="image/png,.png,image/jpeg,.jpg,.jpeg,image/webp,.webp"
                multiple={true}
                tabIndex={-1}
                className="hidden"
                type="file"
                style={{
                    border: 0,
                    clip: "rect(0px, 0px, 0px, 0px)",
                    clipPath: "inset(50%)",
                    height: 1,
                    margin: "0px -1px -1px 0px",
                    overflow: "hidden",
                    padding: 0,
                    position: "absolute",
                    width: 1,
                    whiteSpace: "nowrap"
                }}
                />
                <textarea
                    rows={1}
                    value={message}
                    className="bg-surface-primary box-border w-full flex-none resize-none focus:outline-none active:outline-none max-h-[40vh] p-1 md:p-3"
                    name="message"
                    autoComplete="off"
                    placeholder="Ask followup…"
                    data-sentry-element="AutoResizeTextarea"
                    data-sentry-source-file="evaluation-form.tsx"
                    style={{ height: "48px !important" }}
                    onChange={handleMessageInput}
                    onKeyDown={processKeyboardInput} 
                />
                <div className="flex justify-between gap-4">
                <div className="mr-1 flex h-8 flex-none gap-2">
                    <div
                    className="flex items-center gap-2"
                    data-sentry-component="SelectChatModality"
                    data-sentry-source-file="chat-modality-selector.tsx"
                    >
                    <button
                        className="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ring-offset-2 focus-visible:ring-offset-surface-primary disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 text-interactive-active border border-border-faint bg-transparent active:text-text-tertiary h-8 w-8 p-2 rounded-md active:transition-transform active:duration-75 transition-colors duration-150 ease-out group/modality-button relative hover:text-interactive-active hover:bg-interactive-normal/10 hover:border-interactive-normal/10"
                        type="button"
                        aria-label="Search"
                        data-state="closed"
                        data-sentry-element="TooltipTrigger"
                        data-sentry-source-file="basic-tooltip.tsx"
                    >
                        <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width={24}
                        height={24}
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth={2}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="lucide lucide-globe size-4"
                        >
                        <circle cx={12} cy={12} r={10} />
                        <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20" />
                        <path d="M2 12h20" />
                        </svg>
                    </button>
                    <button
                        className="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ring-offset-2 focus-visible:ring-offset-surface-primary disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 text-interactive-active border border-border-faint bg-transparent active:text-text-tertiary h-8 w-8 p-2 rounded-md active:transition-transform active:duration-75 transition-colors duration-150 ease-out group/modality-button relative hover:text-interactive-active hover:bg-interactive-normal/10 hover:border-interactive-normal/10"
                        type="button"
                        aria-label="Image"
                        data-state="closed"
                        data-sentry-element="TooltipTrigger"
                        data-sentry-source-file="basic-tooltip.tsx"
                    >
                        <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width={24}
                        height={24}
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth={2}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="lucide lucide-image size-4"
                        >
                        <rect width={18} height={18} x={3} y={3} rx={2} ry={2} />
                        <circle cx={9} cy={9} r={2} />
                        <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
                        </svg>
                    </button>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <div
                    data-state="closed"
                    data-sentry-element="TooltipTrigger"
                    data-sentry-source-file="public-notice-button.tsx"
                    >
                    <button
                        type="button"
                        className="text-interactive-normal hover:text-interactive-active focus-visible:text-interactive-active flex cursor-pointer select-none items-center justify-center transition-colors duration-200 rounded-md p-2"
                    >
                        <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width={16}
                        height={16}
                        viewBox="2 2 19 19"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        style={{ overflow: "visible" }}
                        >
                        <g
                            stroke="currentColor"
                            transform-origin="12.013019561767578px 14.971955299377441px"
                            style={{
                            transform: "none",
                            transformOrigin: "12.013px 14.972px"
                            }}
                        >
                            <path d="M11 14h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 16" />
                            <path d="m7 20 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9"></path>
                            <path d="m2 15 6 6" />
                        </g>
                        <path
                            d="M19.5 8.5c.7-.7 1.5-1.6 1.5-2.7A2.73 2.73 0 0 0 16 4a2.78 2.78 0 0 0-5 1.8c0 1.2.8 2 1.5 2.8L16 12Z"
                            strokeWidth="1.5"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            fill="transparent"
                            stroke="currentColor"
                            transform-origin="16.007304191589355px 7.379882335662842px"
                            style={{
                            transform: "none",
                            transformOrigin: "16.0073px 7.37988px"
                            }}
                        />
                        </svg>
                    </button>
                    </div>
                    <button
                    className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ring-offset-2 focus-visible:ring-offset-surface-primary disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 h-8 w-8 active:bg-interactive-cta-active opacity-50 pointer-events-none bg-header-primary hover:bg-header-primary/90 text-interactive-on-cta"
                    disabled={false}
                    type="submit"
                    data-sentry-element="Button"
                    data-sentry-source-file="evaluation-form.tsx"
                    >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width={24}
                        height={24}
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth={2}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="lucide lucide-arrow-up size-4"
                        data-sentry-element="ArrowUp"
                        data-sentry-source-file="evaluation-form.tsx"
                    >
                        <path d="m5 12 7-7 7 7" />
                        <path d="M12 19V5" />
                    </svg>
                    </button>
                </div>
                </div>
            </div>
            <div className="absolute -bottom-5 flex w-full justify-center">
                <p className="text-text-muted whitespace-nowrap text-[10px]">
                Inputs are processed by third-party AI and responses may be inaccurate.
                </p>
            </div>
            </form>
        </div>
    );
}   