import React from "react";
import { useEffect } from "react";

// import { ChatAPI } from "@/api/chat" 
import { ChatAPI } from "@common/api";

import { useChatStore } from 'chat/store'
const ChatMulti = React.lazy(() => import('chat/ChatMulti'));
const ChatSend = React.lazy(() => import('chat/ChatSend'));
const ChatModelSelect = React.lazy(() => import('chat/ChatModelSelect'));

function ChatMultiTest() {

  //let chatComponent = new Chat;

  const chats = ["abcd","bcde", "efgh"];
  const { conversationHistory } = useChatStore();

  useEffect(() => {
    let cancelled = false;

    const listTitle = async () => {
      if (cancelled) return;
      const ret = await ChatAPI.listTitle()
      if (!cancelled && ret) {
        for (const r of ret) {
          console.log('title: title', r.title);
        }
      }
    };
    listTitle();

    const getChat = async () => {
      if (cancelled) return;
      const ret = await ChatAPI.getChat("251027000800003162xe01");
      if (!cancelled && ret) {
        console.log('chat title', ret.title)
        for (const child of ret.children) {
            console.log(" - child:", child.id);
          for (const c of child.children) {
            console.log(" -- child:", c.id, c.user_prompt);
          }
        }
      }
    };
    getChat();

    // cleanup function when component unmounts
    return () => {
      cancelled = true;
    }
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      {/* <Chat chatContentID={"abcd"}/>
      <ChatSend targetID={["abcd"]}/> */}

      {/* <div style={{ display: 'flex', gap: '16px' }}>
        <Chat chatContentID="abcd"/>
        <Chat chatContentID="bcde"/>
        <Chat chatContentID="efgh"/>
      </div>
      <ChatSend targetID={["abcd","bcde", "efgh"]}/> */}

      <div style={{ display: 'flex', gap: '16px', padding: '16px' }}>
        <div style={{ flex: 1 }}>
          <ChatModelSelect chatContentID="abcd" />
        </div>
        <div style={{ flex: 1 }}>
          <ChatModelSelect chatContentID="bcde" />
        </div>
        <div style={{ flex: 1 }}>
          <ChatModelSelect chatContentID="efgh" />
        </div>
      </div>

      <div style={{ flex: 1, overflow: 'auto', padding: '16px' }}>
        {conversationHistory.length > 0 ? (
          // Show conversation history
          conversationHistory.map((query:any, index:any) => (
            <div key={index} style={{ marginBottom: '24px' }}>
              <React.Suspense fallback={<div>Loading Remote App...</div>}>
                <ChatMulti chats={chats} query={query} conversationIndex={index}/>
              </React.Suspense>
            </div>
          ))
        ) : (
          // Show current input being typed when no history
          // <ChatMulti chats={chats}/>
          null
        )}
      </div>
      <div style={{ position: 'sticky', bottom: 0, backgroundColor: 'white' }}>
        <ChatSend targetID={chats}/>
      </div>
    </div>
  )
}

export default ChatMultiTest;
