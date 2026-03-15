import { View, Text } from "react-native";

export default function Alert() {
  return (
    <View style={{flex:1,justifyContent:"center",alignItems:"center"}}>
      <Text style={{fontSize:24,color:"red"}}>
        ⚠ Scam Voice Detected
      </Text>
    </View>
  );
}