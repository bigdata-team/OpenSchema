import { useAuth } from '../contexts/AuthContext';
import { UserProfile } from './UserProfile';
import { useEffect } from 'react';

export function ProtectedPage() {
  const { user, isInitializing, authError, logout, login } = useAuth();

  // 이 페이지는 인증이 필요하므로 자동 리다이렉트
  useEffect(() => {
    if (!isInitializing && !user) {
      const currentUrl = window.location.href;
      console.log('[ProtectedPage] Not authenticated, redirecting to login with redirect_uri:', currentUrl);
      login(currentUrl);
    }
  }, [isInitializing, user, login]);

  // 로딩 중
  if (isInitializing) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">인증 확인 중...</p>
        </div>
      </div>
    );
  }

  // 에러 발생
  if (authError) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-red-600">
          <p>Error: {authError}</p>
        </div>
      </div>
    );
  }

  // 인증된 사용자
  if (user) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 px-4">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-2xl font-bold mb-8">Protected Page - 인증 필요 페이지</h1>

          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4">로그인된 사용자 프로필</h2>
            <UserProfile user={user} onLogout={logout} />
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">DB 사용자 정보 (OpenSchema PostgreSQL)</h2>
            <div className="space-y-2 text-sm">
              <div className="flex">
                <span className="font-medium w-32">User ID:</span>
                <span className="text-gray-700">{user.id}</span>
              </div>
              <div className="flex">
                <span className="font-medium w-32">Email:</span>
                <span className="text-gray-700">{user.email}</span>
              </div>
              <div className="flex">
                <span className="font-medium w-32">Name:</span>
                <span className="text-gray-700">{user.name}</span>
              </div>
              <div className="flex">
                <span className="font-medium w-32">Role:</span>
                <span className="text-gray-700">{user.role || 'N/A'}</span>
              </div>
              <div className="flex">
                <span className="font-medium w-32">Auth Provider:</span>
                <span className="text-gray-700">{user.idp_cd || 'email/password'}</span>
              </div>
              {user.picture && (
                <div className="flex items-start">
                  <span className="font-medium w-32">Picture URL:</span>
                  <span className="text-gray-700 break-all">{user.picture}</span>
                </div>
              )}
            </div>

            <details className="mt-4">
              <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800">
                전체 JSON 데이터 보기
              </summary>
              <pre className="mt-2 p-3 bg-gray-100 rounded text-xs overflow-auto">
                {JSON.stringify(user, null, 2)}
              </pre>
            </details>
          </div>
        </div>
      </div>
    );
  }

  // 인증되지 않은 상태 (리다이렉트 대기 중)
  return null;
}