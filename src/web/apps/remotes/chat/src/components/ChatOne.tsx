import Chat from "@/components/Chat";
import { useChatStore } from "@/store";


export default function ChatOne({
    chats,
    query,
    conversationIndex,
}: {
    chats: string[];
    query?: string; // Optional: if provided, shows specific query; otherwise shows currentInput
    conversationIndex?: number; // Which conversation this is (0, 1, 2, ...)
}) {
  // Get current input from store
  const { currentInput } = useChatStore();

  // Use provided query or currentInput
  const displayQuery = query !== undefined ? query : currentInput;

  return (
    <>
      <div style={{ padding: '8px', marginBottom: '16px', display: 'flex', justifyContent: 'flex-end' }}>
        {displayQuery || <span style={{ color: '#999' }}></span>}
      </div>
      <div style={{ display: 'flex', gap: '16px' }}>
        {chats.map(chat => (
          <div key={chat} style={{ flex: 1, minWidth: 0 }}>
            <Chat chatContentID={chat} conversationIndex={conversationIndex}/>
          </div>
        ))}
      </div>
      {/* <div style={{ display: 'flex', gap: '16px' }}>
        <Chat chatContentID="abcd"/>
        <Chat chatContentID="bcde"/>
        <Chat chatContentID="efgh"/>
      </div> */}
    </>
  )
}