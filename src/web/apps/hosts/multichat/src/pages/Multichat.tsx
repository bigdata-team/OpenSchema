import React from 'react';

/*
const ChatApp = React.lazy(() => import('chat/Chat'));
const ChatSend = React.lazy(() => import('chat/ChatSend'));
*/
const ChatMulti = React.lazy(() => import('chat/ChatMulti'));

function Multichat() {
    return (
        <React.Suspense fallback={<div>Loading Remote App...</div>}>
          {/* <div style={{ display: 'flex', gap: '16px' }}>
            <ChatApp chatContentID="abcd"/>
            <ChatApp chatContentID="bcde"/>
            <ChatApp chatContentID="efgh"/>
          </div>
          <ChatSend targetID={["abcd","bcde", "efgh"]}/> */}
          <ChatMulti />
        </React.Suspense>
    );
}

export default Multichat;