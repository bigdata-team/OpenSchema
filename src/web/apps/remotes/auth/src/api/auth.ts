import axios, {
	AxiosError,
	type AxiosInstance,
	type AxiosRequestConfig,
	type InternalAxiosRequestConfig,
} from "axios";
import useAuth from "@/store/auth";
import type {
	MeResponsePayload,
	RefreshResponsePayload,
	Response,
	SignInRequestPayload,
	SignInResponsePayload,
	SignUpRequestPayload,
	SignUpResponsePayload,
} from "@/types/api";

const GATEWAY_URL = import.meta.env.VITE_ELPAI_GATEWAY_URL ?? "";
const AUTH_BASE_PATH = "/api/v1/auth";
const DEFAULT_HEADERS = {
	"Content-Type": "application/json",
} as const;

type AuthRequestConfig = InternalAxiosRequestConfig & { _retry?: boolean };

type CreateClientOptions = {
	basePath: string;
	withAuth?: boolean;
	config?: AxiosRequestConfig;
};

const createBaseClient = (
	basePath: string,
	config: AxiosRequestConfig = {}
) => {
	const headers = {
		...DEFAULT_HEADERS,
		...(config.headers as Record<string, string> | undefined),
	};

	return axios.create({
		baseURL: `${GATEWAY_URL}${basePath}`,
		withCredentials: true,
		...config,
		headers,
	});
};

const setAuthorizationHeader = (
	config: InternalAxiosRequestConfig,
	token: string
) => {
	if (config.headers?.set) {
		config.headers.set("Authorization", `Bearer ${token}`);
	} else {
		const headers =
			(config.headers as Record<string, string> | undefined) ?? {};

		headers.Authorization = `Bearer ${token}`;
		config.headers = headers as InternalAxiosRequestConfig["headers"];
	}

	return config;
};

let refreshPromise: Promise<string | null> | null = null;

const refreshClient = createBaseClient(AUTH_BASE_PATH);

const refreshAccessToken = async (): Promise<string | null> => {
	if (!refreshPromise) {
		refreshPromise = (async () => {
			try {
				const res = await refreshClient.post<
					Response<SignInResponsePayload>
				>("/refresh");
				const newAccessToken = res.data.data?.access_token ?? null;

				if (newAccessToken) {
					useAuth.setState({ accessToken: newAccessToken });
				}

				return newAccessToken;
			} catch (error) {
				useAuth.setState({
					accessToken: null,
					refreshToken: null,
				});

				return null;
			} finally {
				refreshPromise = null;
			}
		})();
	}

	return refreshPromise;
};

async function authRequestInterceptor(config: InternalAxiosRequestConfig) {
	const authState = useAuth.getState();

	if (authState.accessToken) {
		return setAuthorizationHeader(config, authState.accessToken);
	}

	const newAccessToken = await refreshAccessToken();

	if (newAccessToken) {
		return setAuthorizationHeader(config, newAccessToken);
	}

	return config;
}

const attachAuthInterceptors = (instance: AxiosInstance) => {
	instance.interceptors.request.use(authRequestInterceptor);
	instance.interceptors.response.use(
		(response) => response,
		async (error: AxiosError<Response>) => {
			const status = error.response?.status;
			const originalRequest = error.config as
				| AuthRequestConfig
				| undefined;

			if (status !== 401 || !originalRequest || originalRequest._retry) {
				return Promise.reject(error);
			}

			originalRequest._retry = true;

			const newAccessToken = await refreshAccessToken();

			if (!newAccessToken) {
				return Promise.reject(error);
			}

			setAuthorizationHeader(originalRequest, newAccessToken);

			return instance(originalRequest);
		}
	);

	return instance;
};

export const createClient = ({
	basePath,
	withAuth = false,
	config,
}: CreateClientOptions) => {
	const client = createBaseClient(basePath, config);
	return withAuth ? attachAuthInterceptors(client) : client;
};

const BASE_PATH = AUTH_BASE_PATH;

export const api = createClient({
	basePath: BASE_PATH,
});

export const privateApi = createClient({
	basePath: BASE_PATH,
	withAuth: true,
});

const AuthAPI = {
	signUp: async (payload: SignUpRequestPayload) => {
		const res = await api.post<Response<SignUpResponsePayload>>(
			"/signup",
			payload
		);
		return res.data;
	},
	signIn: async (payload: SignInRequestPayload) => {
		const res = await api.post<Response<SignInResponsePayload>>(
			"/signin",
			payload
		);
		return res.data;
	},
	signOut: async () => {
		const res = await api.post<Response>("/signout");
		return res.data;
	},
	me: async () => {
		const res = await privateApi.get<Response<MeResponsePayload>>("/me");
		return res.data;
	},
	refresh: async () => {
		const res = await privateApi.get<Response<RefreshResponsePayload>>(
			"/refresh"
		);
		return res.data;
	},
};

export default AuthAPI;
