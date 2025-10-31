import { AuthProvider, useAuth } from '../contexts/AuthContext';
import { LoginButton } from '../components/LoginButton';
import { UserProfile } from '../components/UserProfile';

interface AuthWidgetProps {
  gatewayUrl?: string;
  authUrl?: string;
}

function AuthWidgetContent() {
  const { user, isInitializing, logout } = useAuth();

  if (isInitializing) {
    return (
      <div className="p-4 text-center text-sm text-gray-500">
        로딩 중...
      </div>
    );
  }

  return user ? (
    <UserProfile user={user} onLogout={logout} />
  ) : (
    <div className="p-4">
      <LoginButton />
    </div>
  );
}

// AuthProvider로 감싸서 export (Module Federation용)
export function AuthWidget(props: AuthWidgetProps) {
  return (
    <AuthProvider
      gatewayUrl={props.gatewayUrl}
      authUrl={props.authUrl}
      requireAuth={false}
    >
      <AuthWidgetContent />
    </AuthProvider>
  );
}

export default AuthWidget;
