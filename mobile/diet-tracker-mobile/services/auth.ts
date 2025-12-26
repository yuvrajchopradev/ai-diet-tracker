import api from "./api";
import * as SecureStore from "expo-secure-store";

export async function login(email: string, password: string) {
    const res = await api.post("/auth/login", {email, password});
    await SecureStore.setItemAsync("token", res.data.access_token);
} 