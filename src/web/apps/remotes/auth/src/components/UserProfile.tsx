import { Button } from '@/components/ui/button';
import { Avatar } from '@/components/ui/avatar';
import { User } from 'lucide-react';

interface UserData {
  id: string;
  email: string;
  name: string;
  role?: string | null;  // Gateway에서만 제공되므로 optional
  picture?: string | null;
  idp_cd?: string | null;
}

interface UserProfileProps {
  user: UserData;
  onLogout?: () => void;
}

export function UserProfile({ user, onLogout }: UserProfileProps) {
  const handleLogout = () => {
    // 로그아웃 처리 (추후 구현)
    if (onLogout) {
      onLogout();
    }
  };

  return (
    <div className="flex flex-col gap-2 p-4">
      <div className="flex items-center gap-3 mb-2">
        <Avatar className="h-10 w-10">
          {user.picture ? (
            <img src={user.picture} alt={user.name} />
          ) : (
            <div className="flex items-center justify-center h-full w-full bg-gray-200">
              <User className="h-6 w-6 text-gray-500" />
            </div>
          )}
        </Avatar>
        <div className="flex flex-col">
          <span className="text-sm font-medium">{user.name}</span>
          <span className="text-xs text-gray-500">{user.email}</span>
        </div>
      </div>

      {user.idp_cd && (
        <div className="text-xs text-gray-400">
          {user.idp_cd} 로그인
        </div>
      )}

      <Button
        onClick={handleLogout}
        variant="outline"
        size="sm"
        className="w-full mt-2"
      >
        로그아웃
      </Button>
    </div>
  );
}
