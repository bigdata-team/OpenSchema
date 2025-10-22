import { create } from "zustand";

type CountdownState = {
  count: number;
  decrement: () => void;
};

export const useCountdown = create<CountdownState>((set) => ({
  count: 0,
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));

export default useCountdown;
