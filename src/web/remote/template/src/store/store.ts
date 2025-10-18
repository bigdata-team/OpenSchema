import { create } from "zustand";

interface CountState {
  count: number;
  inc: () => void;
  reset: () => void;
}

interface NameState {
  name: string;
  change: (newName: string) => void;
  reset: () => void;
}

export const useCountStore = create<CountState>((set) => ({
  count: 0,
  inc: () => set((state: CountState) => ({ count: state.count + 1 })),
  reset: () => set({ count: 0 }),
}));

export const useNameStore = create<NameState>((set) => ({
  name: '',
  change: (newName: string) => set((state: NameState) => ({ name: state.name + newName })),
  reset: () => set({ name: '' }),
}));