import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { ShieldAlert } from 'lucide-react-native';

export default function VoiceGuardApp() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <ShieldAlert size={100} color="#00f2ff" />
      <Text style={styles.brandTitle}>Vigilance AI</Text>
      <TouchableOpacity 
        style={styles.simulateBtn} 
        onPress={() => router.push('/incoming-call')}
      >
        <Text style={styles.btnText}>Start AI Protection</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000814', justifyContent: 'center', alignItems: 'center' },
  brandTitle: { color: 'white', fontSize: 32, fontWeight: 'bold', marginTop: 20 },
  simulateBtn: { backgroundColor: '#00ffaa', paddingVertical: 15, paddingHorizontal: 40, borderRadius: 30, marginTop: 40 },
  btnText: { fontWeight: 'bold', fontSize: 16, color: '#000' }
});