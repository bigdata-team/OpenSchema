/**
 * ElpaiAuth Service
 * elpai-auth SDK를 래핑한 서비스 클래스
 */

import { loadElpaiAuthSDK, getElpaiAuthClass } from '../lib/auth-sdk-loader';
import type { ElpaiAuthInstance } from '../lib/auth-sdk-loader';

export interface User {
  id: string;
  email: string;
  name: string;
  role?: string | null;  // Gateway에서만 제공되므로 optional
  picture?: string | null;
  idp_cd?: string | null;
}

class ElpaiAuthService {
  private authUrl: string;
  private authInstance: ElpaiAuthInstance | null = null;
  private isInitialized = false;

  constructor(authUrl: string = import.meta.env.VITE_ELPAI_AUTH_URL) {
    this.authUrl = authUrl;
    console.log('[ElpaiAuthService] Created with authUrl:', this.authUrl);
  }

  async init(): Promise<void> {
    if (this.isInitialized && this.authInstance) return;

    try {
      // SDK 로드
      await loadElpaiAuthSDK(this.authUrl);

      // ElpaiAuth 클래스 가져오기
      const ElpaiAuthClass = getElpaiAuthClass();
      if (!ElpaiAuthClass) {
        throw new Error('ElpaiAuth class not available');
      }

      // 인스턴스 생성
      this.authInstance = new ElpaiAuthClass({
        authUrl: this.authUrl,
        cacheTimeout: 3600 // 1시간 캐시
      });

      this.isInitialized = true;
      console.log('[ElpaiAuthService] SDK instance created');
    } catch (error) {
      console.error('[ElpaiAuthService] Failed to initialize SDK:', error);
      throw error;
    }
  }

  async getUserInfo(): Promise<User | null> {
    await this.init();

    if (!this.authInstance) {
      console.error('[ElpaiAuthService] Auth instance not available');
      return null;
    }

    try {
      const userInfo: any = await this.authInstance.getUserInfo(false);
      console.log('[ElpaiAuthService] Raw SDK response:', userInfo);

      if (userInfo) {
        // SDK 응답을 User 타입으로 매핑
        // SDK 응답 필드 확인: sub, subject, id 등 가능한 필드 시도
        return {
          id: userInfo.sub || userInfo.subject || userInfo.id || userInfo.email,
          email: userInfo.email,
          name: userInfo.name,
          picture: userInfo.picture || null,
          idp_cd: null, // SDK는 idp_cd를 제공하지 않음
        };
      }
      return null;
    } catch (error: any) {
      // 401은 정상적인 "인증 안됨" 상태이므로 에러 로그 생략
      if (error?.message?.includes('401') || error?.status === 401) {
        console.log('[ElpaiAuthService] User not authenticated (401)');
      } else {
        console.error('[ElpaiAuthService] Failed to get user info:', error);
      }
      return null;
    }
  }

  isAuthenticated(): boolean {
    // SDK가 로드되기 전에는 false 반환
    if (!this.authInstance) return false;

    try {
      // isAuthenticated는 동기 메서드
      return this.authInstance.isAuthenticated();
    } catch (error) {
      console.error('[ElpaiAuthService] Failed to check authentication:', error);
      return false;
    }
  }

  login(redirectUri?: string): void {
    if (this.authInstance) {
      this.authInstance.login(redirectUri || window.location.href);
    } else {
      // SDK가 로드되지 않았을 경우 직접 리다이렉트
      const targetRedirectUri = redirectUri || window.location.href;
      window.location.href = `${this.authUrl}/sign-in?redirect_uri=${encodeURIComponent(targetRedirectUri)}`;
    }
  }

  async logout(): Promise<void> {
    if (this.authInstance) {
      try {
        await this.authInstance.logout();
      } catch (error) {
        console.error('[ElpaiAuthService] Logout failed:', error);
      }
    }

    // 로그아웃 후 auth 페이지로 리다이렉트
    // TODO window.location.href = '/ui/v1/auth';
  }

  clearCache(): void {
    if (this.authInstance) {
      this.authInstance.clearCache();
    }
  }
}

// 싱글톤 인스턴스
let instance: ElpaiAuthService | null = null;

export function getElpaiAuthService(authUrl?: string): ElpaiAuthService {
  if (!instance) {
    instance = new ElpaiAuthService(authUrl);
  }
  return instance;
}

export default ElpaiAuthService;