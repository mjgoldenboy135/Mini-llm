"use client";
import { create } from "zustand";
import api from "@/lib/api";
import { User } from "@/types";

interface AuthState {
  user: User | null;
  loading: boolean;
  login: (mobile: string, password: string) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  loading: false,

  login: async (mobile, password) => {
    set({ loading: true });
    const { data } = await api.post("/auth/login/", { mobile, password });
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    set({ user: data.user, loading: false });
  },

  logout: () => {
    localStorage.clear();
    set({ user: null });
  },

  fetchMe: async () => {
    try {
      const { data } = await api.get("/auth/me/");
      set({ user: data });
    } catch {
      set({ user: null });
    }
  },
}));
