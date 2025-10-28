import { useEffect } from "react";
import { useChatStore } from "@/store";

import ChatSend from "@/components/ChatSend";
// import Chat from "@/components/Chat";
import ChatMulti from "@/components/ChatMulti";
import ChatModelSelect from "@/components/ChatModelSelect";
import { ChatAPI } from "@/api/chat";

function ChatMultiTest() {

  //let chatComponent = new Chat;

  const chats = ["abcd","bcde", "efgh"];
  const { conversationHistory } = useChatStore();

  useEffect(() => {
    const fetchData = async () => {
      const ret = await ChatAPI.get("251027000800003162xe01");
      if (ret) {
        console.log('title', ret.title)
        for (const child of ret.children) {
            console.log(" - child:", child.id);
          for (const c of child.children) {
            console.log(" -- child:", c.id, c.user_prompt);
          }
        }
      }
    };
    fetchData();
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
          conversationHistory.map((query, index) => (
            <div key={index} style={{ marginBottom: '24px' }}>
              <ChatMulti chats={chats} query={query} conversationIndex={index}/>
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
