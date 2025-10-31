import { Button } from '@/components/ui/button';
import { useAuth } from '../contexts/AuthContext';

export function LoginButton() {
  const { login } = useAuth();

  const handleLogin = () => {
    // AuthContext의 login 메서드 사용 (SDK 방식)
    console.log('[LoginButton] Initiating login via SDK');
    login();
  };

  return (
    <Button
      onClick={handleLogin}
      variant="default"
      className="w-full"
    >
      로그인
    </Button>
  );
}
