export interface Response<T = null> {
	detail?: string;
	timestamp?: string;
	data: T | null;
}

export interface SignUpRequestPayload {
	email: string;
	password: string;
}

export interface SignUpResponsePayload {
	id: string;
	created_at: string;
	updated_at: string;
	deleted_at: string | null;
	name: string | null;
	email: string;
	hashed_password: string;
	bio: string | null;
	role: string;
}

export interface SignInRequestPayload {
	email: string;
	password: string;
}

export interface SignInResponsePayload {
	access_token: string;
	refresh_token: string;
}

export type MeResponsePayload = SignUpResponsePayload;
export type RefreshResponsePayload = SignInResponsePayload;
