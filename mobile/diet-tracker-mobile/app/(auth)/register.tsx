import api from "@/services/api";
import { useRouter } from "expo-router";
import { useState } from "react";
import { Button, TextInput, View } from "react-native";

export default function Register() {
    const router = useRouter();

    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [name, setName] = useState<string>("");

    const handleRegister = () => {
        api.post("/auth/register", { email, password, name })
            .then(() => {
                router.replace("/(auth)/login");
            })
    }

    return (
        <View>
            <TextInput
                placeholder="Name"
                onChangeText={(v) => setName(v)}
            />
            <TextInput
                placeholder="Email"
                onChangeText={(v) => setEmail(v)}
            />
            <TextInput
                placeholder="Password"
                onChangeText={(v) => setPassword(v)}
            />

            <Button title="Register" onPress={handleRegister} />
        </View>
    )
}