import React, { useEffect } from 'react';
import { useAuth } from 'auth/AuthContext';
import { useNavigate } from 'react-router';

const LoginRemote = React.lazy(() => import('auth/Login'));

function Login() {
  const { user, isInitializing } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isInitializing && user) {
      console.log('[Login] User is already logged in')
      // TODO
      // navigate('/');
    } 
  }, [user, isInitializing, navigate]);

  return (
    <div className='p-2'>
      <React.Suspense fallback={<div>Loading Remote App...</div>}>
        <LoginRemote />
      </React.Suspense>
    </div>
  )
}

export default Login;