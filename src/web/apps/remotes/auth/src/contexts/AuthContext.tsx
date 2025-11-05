'use client';

import { createContext, useContext, useCallback, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { getElpaiAuthService } from '../services/elpai-auth.service';
import type { User } from '../services/elpai-auth.service';
import { user }  from '@common/api';
import { Config } from '@common/config';

interface AuthState {
  isAuthenticated: boolean;
  isInitializing: boolean;
  user: User | null;
  authError: string | null;
}

interface AuthContextType extends AuthState {
  checkAuth: (options?: {
    isPageLoad?: boolean;
    forceRefresh?: boolean;
  }) => Promise<boolean>;
  login: (returnUrl?: string) => void;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
  gatewayUrl?: string;
  authUrl?: string;
  requireAuth?: boolean; // true인 경우 인증되지 않으면 자동 리다이렉트
}

export function AuthProvider({
  children,
  gatewayUrl = import.meta.env.VITE_ELPAI_GATEWAY_URL,
  authUrl = import.meta.env.VITE_ELPAI_AUTH_URL,
  requireAuth = false
}: AuthProviderProps) {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    isInitializing: true,
    user: null,
    authError: null,
  });

  const authService = getElpaiAuthService(authUrl);

  const checkAuth = useCallback(async (options: {
    isPageLoad?: boolean;
    forceRefresh?: boolean;
  } = {}): Promise<boolean> => {
    const { isPageLoad = false } = options;

    try {
      console.log('[AuthProvider] Checking authentication via SDK...');

      // SDK 초기화
      await authService.init();

      // getUserInfo를 먼저 호출해서 실제 인증 상태를 확인 (캐시 생성)
      const userInfo = await authService.getUserInfo();
      console.log('[AuthProvider] User info from SDK:', userInfo);

      // userInfo가 있으면 인증된 것
      if (userInfo) {
        console.log('[AuthProvider] User authenticated via SDK');

        // Gateway를 통해 OpenSchema DB에 사용자 동기화
        try {
            // TODO const response = await fetch(`${gatewayUrl}/api/v1/auth/signin/sso`, {
            const response = await fetch(`${Config.value('API_GATEWAY_URL')}/api/v1/auth/signin/sso`, {
              credentials: 'include',
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
              }
            });

            // 401/403은 인증 실패, SDK 캐시 초기화 필요
            if (!response || response.status === 401 || response.status === 403) {
              console.log('[AuthProvider] Gateway auth failed, clearing SDK cache');
              authService.clearCache();
              setAuthState({
                isAuthenticated: false,
                isInitializing: false,
                user: null,
                authError: null,
              });
              return false;
            }

            if (response.ok) {
              const data = await response.json();
              if (data.data) {
                // Gateway 응답에서 ID, role, idp_cd 가져오고, 나머지는 SDK 데이터 사용
                const mergedUser = {
                  ...userInfo,  // SDK 데이터 (한글 정상)
                  id: data.data.id,  // DB에서 생성된 ID
                  role: data.data.role || userInfo.role,  // DB의 role 사용
                  idp_cd: data.data.idp_cd || userInfo.idp_cd,  // DB의 idp_cd 사용 (google, github 등)
                };

                // TODO
                user.login(data.data.access_token);

                setAuthState({
                  isAuthenticated: true,
                  isInitializing: false,
                  user: mergedUser,
                  authError: null,
                });
                console.log('[AuthProvider] User synced with OpenSchema DB:', mergedUser);
                return true;
              }
            }

            // 500 에러 등 서버 문제시 SDK 데이터만 사용
            if (response.status >= 500) {
              console.log('[AuthProvider] Gateway server error, using SDK data only');
            }
          } catch (error) {
            console.log('[AuthProvider] Failed to sync with OpenSchema DB, using SDK data');
          }

          // Gateway 동기화 실패시 SDK 데이터 사용
          setAuthState({
            isAuthenticated: true,
            isInitializing: false,
            user: userInfo,
            authError: null,
          });
          return true;
      }

      // 인증되지 않은 경우
      console.log('[AuthProvider] User not authenticated');

      // TODO temp code
      if (import.meta.env.DEV) {
        console.log('[AuthProvider] User not authenticated but in DEV mode, skipping error');
        // TODO
        user.login(Config.value("TEMP_ACCESS_TOKEN"));
        setAuthState({
          isAuthenticated: true,
          isInitializing: false,
          user: { id: 'TODO-id', name: 'TODO User', email: 'TODO@example.com' } as User,
          authError: null,
        });
        return true;
      }

      // requireAuth가 true이고 페이지 로드시 인증 실패하면 로그인 페이지로 리다이렉트
      if (requireAuth && isPageLoad && typeof window !== 'undefined') {
        authService.login(window.location.href);
      } else {
        // 인증 실패 상태만 설정
        setAuthState({
          isAuthenticated: false,
          isInitializing: false,
          user: null,
          authError: null,
        });
      }

      return false;
    } catch (error) {
      console.error('[AuthProvider] Authentication check failed:', error);

      // 에러 발생시 처리
      if (requireAuth && isPageLoad && typeof window !== 'undefined') {
        authService.login(window.location.href);
      } else {
        setAuthState({
          isAuthenticated: false,
          isInitializing: false,
          user: null,
          authError: error instanceof Error ? error.message : 'Authentication check failed',
        });
      }

      return false;
    }
  }, [authService, gatewayUrl, requireAuth]);

  const login = useCallback((returnUrl?: string) => {
    authService.login(returnUrl);
  }, [authService]);

  const logout = useCallback(async () => {
    await authService.logout();

    // 상태 초기화
    setAuthState({
      isAuthenticated: false,
      isInitializing: false,
      user: null,
      authError: null,
    });
  }, [authService]);

  // 컴포넌트 마운트시 인증 체크
  useEffect(() => {
    console.log('[AuthContext] Component mounted, checking auth...');
    checkAuth({ isPageLoad: true });
  }, [checkAuth]);

  const contextValue: AuthContextType = {
    ...authState,
    checkAuth,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}