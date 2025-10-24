import ChatSend from "@/components/ChatSend";
// import Chat from "@/components/Chat";
import ChatOne from "@/components/ChatOne";
import { useChatStore } from "@/store";
import ChatModelSelect from "@/components/ChatModelSelect";

function ChatMulti() {

  //let chatComponent = new Chat;

  const chats = ["abcd","bcde", "efgh"];
  const { conversationHistory } = useChatStore();

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
              <ChatOne chats={chats} query={query} conversationIndex={index}/>
            </div>
          ))
        ) : (
          // Show current input being typed when no history
          // <ChatOne chats={chats}/>
          null
        )}
      </div>
      <div style={{ position: 'sticky', bottom: 0, backgroundColor: 'white' }}>
        <ChatSend targetID={chats}/>
      </div>
    </div>
  )
}

export default ChatMulti;
