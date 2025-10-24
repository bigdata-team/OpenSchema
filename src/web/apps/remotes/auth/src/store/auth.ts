import { create } from "zustand";
import type {} from "@/types/api";

type Tokens = {
	accessToken: string | null;
	refreshToken: string | null;
};

type AuthState = {
	isLoading: boolean;
	accessToken: string | null;
	refreshToken: string | null;
};

export const useAuth = create<AuthState>((set) => ({
	isLoading: false,
	accessToken: null,
	refreshToken: null,
	setTokens: (tokens: Tokens) =>
		set(() => ({
			accessToken: tokens.accessToken,
			refreshToken: tokens.refreshToken,
		})),
}));

export default useAuth;
