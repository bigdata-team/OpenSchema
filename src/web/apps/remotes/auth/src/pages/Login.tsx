import { useAuth } from '@/contexts/AuthContext';
import { LoginButton } from '@/components/LoginButton';
import { UserProfile } from '@/components/UserProfile';

function Login() {
  const { user, isInitializing, logout } = useAuth();

  return (
    <div className='p-4 max-w-2xl mx-auto'>
      {isInitializing ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">인증 상태 확인 중...</p>
        </div>
      ) : user ? (
        <div>
          <h2 className='text-xl font-semibold mb-4'>로그인된 사용자 정보</h2>
          <UserProfile user={user} onLogout={logout} />

          <div className='mt-6 p-4 bg-gray-100 rounded-lg'>
            <h3 className='font-semibold mb-2'>DB에서 가져온 사용자 정보:</h3>
            <div className='bg-white p-3 rounded text-sm'>
              <p><strong>ID:</strong> {user.id}</p>
              <p><strong>Email:</strong> {user.email}</p>
              <p><strong>Name:</strong> {user.name}</p>
              <p><strong>Role:</strong> {user.role}</p>
              <p><strong>Provider:</strong> {user.idp_cd || 'email'}</p>
              {user.picture && <p><strong>Picture:</strong> {user.picture}</p>}
            </div>
            <details className='mt-3'>
              <summary className='cursor-pointer text-sm text-gray-600'>Raw JSON</summary>
              <pre className='text-xs mt-2 overflow-auto bg-white p-2 rounded'>
                {JSON.stringify(user, null, 2)}
              </pre>
            </details>
          </div>
        </div>
      ) : (
        <div className='text-center py-8'>
          <p className='mb-6 text-gray-600'>로그인이 필요합니다</p>
          <LoginButton />
        </div>
      )}
    </div>
  )
}

export default Login;
