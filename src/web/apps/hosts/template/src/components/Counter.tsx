// import { useCounter } from 'remote/store'
import { useCounter } from 'chat/store'

type CounterProps = {
  useCounterHook?: typeof useCounter;
};

type CounterState = {
  count: number;
  increment: () => void;
}

function Counter({ useCounterHook = useCounter }: CounterProps = {}) {
  const count = useCounterHook((state: CounterState) => state.count);
  const increment = useCounterHook((state: CounterState) => state.increment);

  return (
    <div className='m-2'>
      <button
        className="p-2 bg-blue-500 text-white"
        onClick={increment}
      >
        Count is {count}
      </button>
    </div>
  );
}

export default Counter;