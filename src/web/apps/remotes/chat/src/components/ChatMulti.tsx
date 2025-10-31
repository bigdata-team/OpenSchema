import ChatOne from "@/components/ChatOne";
import { Chat } from "@/model/chat";

export default function ChatMulti({
    titleId,
    chat,
    modelCount,
    query,
}: {
    titleId: string;
    chat: Chat;
    modelCount: number;
    query: string;
}) {
  return (
    <>
      <div className="p-2 mb-3 flex justify-end">
        {query ? (
          <span className="bg-gray-50 px-3 py-1 rounded-md text-sm">
            {query}
          </span>
        ) : (
          <span className="text-muted-foreground"></span>
        )}
      </div>
      <div className="flex gap-4">
        {Array.from({ length: modelCount }).map((_, modelIndex) => (
          <div key={modelIndex} className="flex-1 min-w-0">
            <ChatOne titleId={titleId} chat={chat} modelIndex={modelIndex}/>
          </div>
        ))}
      </div>
    </>
  )
}