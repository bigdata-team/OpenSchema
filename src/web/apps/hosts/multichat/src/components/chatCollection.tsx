/*
import React from 'react';
import Chat from "chat/Chat";
import SendChat from "chat/SendChat";

export default function chatCollection({
}: {
})
{
    return (
        <>
            <div className="flex flex-grow flex-col flex-1 h-full justify-between align-center">
                <div className="grid grid-cols-2 gap-10 justify-start">
                    {
                        chatArray.chatList.map((chat,i) => {
                            return (<Chat chatContentID={`chat${i}`} chatting={chat}></Chat>);
                        })
                    }
                </div>
                <SendChat targetID={chatArray.chatList.map((chat,i) => {return `chat${i}`;})} sendFunction={processChat}/>
            </div>
        </>
    );
}
*/