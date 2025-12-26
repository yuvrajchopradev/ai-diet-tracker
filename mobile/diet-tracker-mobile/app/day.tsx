import { useLocalSearchParams } from "expo-router";
import { Text, View } from "react-native";

export default function DayScreen() {
    const {year, month} = useLocalSearchParams();

    return (
        <View>
            <Text>Dates for {month}/{year}</Text>
        </View>
    )
}