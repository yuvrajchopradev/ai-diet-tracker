import { View, Text, Pressable } from "react-native";
import { useEffect, useState } from "react";
import api from "@/services/api";
import { useRouter } from "expo-router";

type MonthItem = {
  year: number;
  month: number;
};

export default function HomeScreen() {
  const [months, setMonths] = useState<MonthItem[]>([]);
  const router = useRouter();

  useEffect(() => {
    api.get("/food/months")
    .then((res) => {
      setMonths(res.data);
    })
    .catch(error => {
      console.log(error);
    });
  }, []);

  return (
    <View>
      {months.map((m) => (
        <Pressable
          key={`${m.year}-${m.month}`}
          onPress={() =>
            router.push({
              pathname: "/day",
              params: { year: m.year, month: m.month },
            })
          }
        >
          <Text>{m.month} / {m.year}</Text>
        </Pressable>
      ))}
    </View>
  );
}