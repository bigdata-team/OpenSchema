import { create } from "zustand";

type NotificationState = {
  titlesChanged: number;
  notifyTitlesChanged: () => void;
}

export const useNotificationStore = create<NotificationState>((set) => ({
  titlesChanged: 0,

  notifyTitlesChanged: () => set((state) => ({
    titlesChanged: state.titlesChanged + 1
  })),
}));

export default useNotificationStore;
