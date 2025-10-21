import SendChat from "@/components/SendChat";
import Chat from "@/components/Chat";

function ChatTest() {

  //let chatComponent = new Chat;
  
  return (
    <>
      <Chat chatContentID={"abcd"}/>
      <SendChat />
    </>
  )
}

export default ChatTest;
