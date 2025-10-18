// import { useState } from 'react';
import { useCountStore } from "../../store/store";

const Counter = () => {
	// const [count, setCount] = useState<number>(0);
	const count = useCountStore((state) => state.count);
	const inc = useCountStore((state) => state.inc);

	return (
		<button
			style={{
				border: '0 solid #e2e8f0',
				marginTop: '10px',
				backgroundColor: 'rgb(246, 179, 82)',
				borderRadius: '.25rem',
				fontWeight: '700',
				padding: '.5rem 1rem .5rem 1rem',
				color: 'rgb(24, 24, 24)',
			}}
			onClick={() => inc()}
		>
			Remote counter: {count}
		</button>
	);
};

export default Counter;