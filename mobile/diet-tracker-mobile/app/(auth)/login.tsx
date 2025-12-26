import { login } from "@/services/auth";
import { useRouter } from "expo-router";
import { useState } from "react";
import { Button, TextInput, View } from "react-native";

export default function Login() {
    const router = useRouter();

    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const handleLogin = () => {
        login(email, password)
            .then(() => {
                router.replace("/(tabs)");
            })
    }

    return (
        <View>
            <TextInput
                placeholder="Email"
                onChangeText={(v) => setEmail(v)}
            />
            <TextInput
                placeholder="Password"
                onChangeText={(v) => setPassword(v)}
            />

            <Button title="Login" onPress={handleLogin} />
        </View>
    )
}