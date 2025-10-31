import ChatSend from "@/components/ChatSend";
import ChatOne from "@/components/ChatOne";
import { Chat } from "@/model/chat";

function ChatTest() {

  //let chatComponent = new Chat;

  const chat = new Chat();

  return (
    <>
      <ChatOne titleId={"TODO"} chat={chat} modelIndex={0}/>
      <ChatSend titleId={"TODO"} models={[]}/>
    </>
  )
}

export default ChatTest;
