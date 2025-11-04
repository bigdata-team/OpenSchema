import { useEffect, useState } from "react";
import { useSearchParams } from "react-router";

import ChatSend from "@/components/ChatSend";
import ChatMulti from "@/components/ChatMulti";
import ChatModelSelect from "@/components/ChatModelSelect";
import { chatManager } from "@/model/chatManager";
import { Chat } from "@/model/chat";
import { modelManager } from "@/model/modelManager";

function ChatMultiTest() {
  const [searchParams] = useSearchParams();
  let titleId = searchParams.get('id');

  const [ chats, setChats ] = useState<Array<Chat>>([]);

  const addNewChat = async (newId: string|null) => { 
    if (!titleId && newId) {
      // New Chat
      titleId = newId;
    }
    const temp = await chatManager.getChildrenByTitleId(titleId??"");
    setChats(() => [...temp]);
  };

  useEffect(() => {
    console.log("ChatMultiTest mounted", titleId);
    let cancelled = false;

    const fetchData = async () => {
      if (!cancelled) {
        if (!titleId) {
          // New Chat
          setChats([]);
        } else {
          let title = await chatManager.getTitleById(titleId);
          if (!title) {
            console.warn("Title not found in ChatManager:", titleId);
            return;
          }
          if (cancelled) return;
          const result = await chatManager.fetchChildrenForTitle(title.id);
          if (cancelled) return;
          if (result) {
          }

          const chats = await chatManager.getChildrenByTitleId(titleId??"");
          setChats(chats);
        }
      }
    };
    fetchData();

    // cleanup function when component unmounts
    return () => {
      cancelled = true;
    };
  }, [titleId]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100%' }}>
      <div style={{ display: 'flex', gap: '16px', padding: '10px' }}>
        {modelManager.models.map((model) => (
          <div key={model.model} style={{ flex: 1 }}>
            <ChatModelSelect model={model}/>
          </div>
        ))}
      </div>

      <div style={{ flex: 1, overflow: 'auto', padding: '10px' }}>
        {chats.map((chat, index) => (
            // console.log("Rendering ChatMulti for chat:", index, chat.user_prompt, chats.length),
            <div key={index} style={{ marginBottom: '24px' }}>
              <ChatMulti titleId={titleId??""} chat={chat} modelCount={modelManager.models.length} query={chat.user_prompt??""}/>
            </div>
          ))}
      </div>
      <div style={{ position: 'sticky', bottom: 0, backgroundColor: 'white' }}>
        <ChatSend titleId={titleId} models={modelManager.models} onNewChat={addNewChat}/>
      </div>
    </div>
  )
}

export default ChatMultiTest;
