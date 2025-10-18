import { Suspense, lazy } from 'react';

const Remote = lazy(
    async () => {
        // @ts-expect-error: remote module provided by host/module-federation at runtime
        return import('remote/remote-app');
    },
);

/*
const Remote2 = lazy(
    // @ts-expect-error: remote module provided by host/module-federation at runtime
	async () => import('remote2/remote-app'),
);
*/

export default function Home() {
    return (
        <div>
            <h2>Home</h2>

            <Suspense fallback="loading...">
				<Remote />
			</Suspense>
            {/*
            <Suspense fallback="loading...">
				<Remote2 />
			</Suspense> */}
        </div>
    );
}   