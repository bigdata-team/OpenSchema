/**
 * Elpai Auth SDK Loader
 * 동적으로 elpai-auth SDK를 로드하고 초기화
 */

export interface ElpaiAuthInstance {
  login: (returnUrl?: string) => void;
  logout: () => Promise<void>;
  isAuthenticated: () => boolean;
  getUserInfo: (forceRefresh?: boolean) => Promise<any>;
  clearCache: () => void;
}

interface ElpaiAuthConfig {
  authUrl: string;
  cacheTimeout?: number;
}

interface ElpaiAuthClass {
  new (config: ElpaiAuthConfig): ElpaiAuthInstance;
}

declare global {
  interface Window {
    ElpaiAuth: ElpaiAuthClass;
  }
}

let sdkLoadPromise: Promise<void> | null = null;

export async function loadElpaiAuthSDK(authUrl: string): Promise<void> {
  // 이미 로드 중이거나 로드됐으면 기다리거나 반환
  if (sdkLoadPromise) {
    return sdkLoadPromise;
  }

  if (window.ElpaiAuth) {
    return Promise.resolve();
  }

  sdkLoadPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = `${authUrl}/sdk/elpai-auth.js`;
    script.async = true;

    script.onload = () => {
      if (window.ElpaiAuth) {
        console.log('[SDK Loader] ElpaiAuth SDK loaded successfully');
        resolve();
      } else {
        reject(new Error('ElpaiAuth SDK failed to load'));
      }
    };

    script.onerror = () => {
      reject(new Error('Failed to load ElpaiAuth SDK'));
    };

    document.head.appendChild(script);
  });

  return sdkLoadPromise;
}

export function getElpaiAuthClass(): ElpaiAuthClass | null {
  return window.ElpaiAuth || null;
}