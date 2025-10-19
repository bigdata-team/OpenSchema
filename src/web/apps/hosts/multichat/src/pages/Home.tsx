import Counter from '@/components/Counter';
import React from 'react';

// const RemoteCounter = React.lazy(() => import('remote/Counter'));
const RemoteCounter = React.lazy(() => import('chat/Counter'));

function Home() {
  return (
    <div className='p-2'>
      <h1>This is home page</h1>
      <p>Welcome to the home page of our application!</p>
      <Counter />
      <React.Suspense fallback={<div>Loading Remote App...</div>}>
        <RemoteCounter />
      </React.Suspense>
    </div>
  )
}

export default Home;
