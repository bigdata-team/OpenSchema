import { useEffect } from "react";
import { useChatStore } from "@/store";

import ChatSend from "@/components/ChatSend";
// import Chat from "@/components/Chat";
import ChatMulti from "@/components/ChatMulti";
import ChatModelSelect from "@/components/ChatModelSelect";
import { ChatAPI } from "@common/api";

function ChatMultiTest() {

  //let chatComponent = new Chat;

  const chats = ["abcd","bcde", "efgh"];
  const { conversationHistory } = useChatStore();

  useEffect(() => {
    console.log("ChatMultiTest mounted");
    let cancelled = false;

    /*
    const createTitle = async () => {
      const ret = await ChatAPI.createTitle("New Title");
      if (ret) {
        console.log('createTitle', ret.id)
      }
    };

    const deleteTitle = async () => {
      const ret = await ChatAPI.deleteTitle("251027050355211441GQ05");
      if (ret) {
        console.log('deleteTitle', ret.id)
      }
    };

    const updateTitle = async () => {
      const ret = await ChatAPI.updateTitle("251027050355211441GQ05", "Updated Title");
      if (ret) {
        console.log('updateTitle', ret.id)
      }
    };

    const createChat = async () => {
      const ret = await ChatAPI.createChat("251027050355211441GQ05")
      if (ret) {
        console.log('createChat', ret.id)
      }
    };
    */

    const getChat = async () => {
      if (cancelled) return;
      const ret = await ChatAPI.getChat("251027000800003162xe01");
      if (ret && !cancelled) {
        console.log('title', ret.title)
        for (const child of ret.children) {
            console.log(" - child:", child.id);
          for (const c of child.children) {
            console.log(" -- child:", c.id, c.user_prompt);
          }
        }
      }
    };

    /*
    const conversations = async () => {
      const data = {
        "parent_id": "251028013129009387kH14",
        "model": "openai/gpt-5",
        "messages": [
          {
            "role": "user",
            "content": "한국 수도"
          }
        ],
        "stream": true,
        "system_prompt": null,
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 50
      }
      const ret = await ChatAPI.conversations(data);
      if (ret) {
        console.log('conversations', ret.id)
      }
    };
    */

    // createTitle();
    // deleteTitle();
    // updateTitle();
    // createChat();
    // conversations();
    getChat();

    // cleanup function when component unmounts
    return () => {
      cancelled = true;
    };
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
