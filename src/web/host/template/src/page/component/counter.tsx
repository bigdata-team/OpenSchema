import { Button } from "@/components/ui/button"

import { useCountStore } from "../../store/store";
import { useNameStore } from "../../store/store";

function Counter() {
  const count = useCountStore(state => state.count);
  const inc = useCountStore(state => state.inc);
  const reset = useCountStore(state => state.reset);

  const name = useNameStore(state => state.name);
  const change = useNameStore(state => state.change);
  const reset2 = useNameStore(state => state.reset);

  return (
    <div>
      <div>Count: {count}</div>
      <Button onClick={inc}>+1</Button>
      <Button onClick={reset}>reset</Button>

      <div>Name: {name}</div>
      <Button onClick={() => change('TODO')}>Change Name</Button>
      <Button onClick={reset2}>reset</Button>
    </div>
  );
}

export default Counter;