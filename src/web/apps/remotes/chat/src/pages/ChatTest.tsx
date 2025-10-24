import ChatSend from "@/components/ChatSend";
import Chat from "@/components/Chat";

function ChatTest() {

  //let chatComponent = new Chat;

  return (
    <>
      <Chat chatContentID={"abcd"}/>
      <ChatSend targetID={["abcd"]}/>
    </>
  )
}

export default ChatTest;
