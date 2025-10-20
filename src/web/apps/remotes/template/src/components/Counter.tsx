import useCounter from '@/store/counter';


type CounterProps = {
  useCounterHook?: typeof useCounter;
};

function Counter({ useCounterHook = useCounter }: CounterProps = {}) {
  const count = useCounterHook((state) => state.count);
  const increment = useCounterHook((state) => state.increment);

  return (
    <div className='m-2'>
      <button
        className="p-2 bg-blue-500 text-white"
        onClick={increment}
      >
        Remote count is {count}
      </button>
    </div>
  );
}

export default Counter;