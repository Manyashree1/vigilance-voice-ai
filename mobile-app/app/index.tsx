import { View, Text } from "react-native";
import { useRouter } from "expo-router";
import { useEffect } from "react";

export default function Index() {

  const router = useRouter();

  useEffect(() => {
    setTimeout(() => {
      router.replace("/login");
    }, 2000);
  }, []);

  return (
    <View style={{flex:1,justifyContent:"center",alignItems:"center"}}>
      <Text>Vigilance Voice AI</Text>
    </View>
  );
}