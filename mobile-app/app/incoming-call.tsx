import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import { MotiView } from 'moti';
import { PhoneIncoming, PhoneOff, User } from "lucide-react-native";
import { LinearGradient } from 'expo-linear-gradient';

export default function IncomingCall() {
  const router = useRouter();

  return (
    <LinearGradient colors={['#001d3d', '#000814']} style={styles.container}>
      
      {/* Caller Icon with Pulse Animation */}
      <View style={styles.callerIconContainer}>
        <MotiView
          from={{ scale: 0.8, opacity: 0.3 }}
          animate={{ scale: 1.5, opacity: 0 }}
          transition={{ loop: true, duration: 1500, type: 'timing' }}
          style={styles.pulse}
        />
        <View style={styles.iconCircle}>
          <User size={60} color="#fff" strokeWidth={1.5} />
        </View>
      </View>

      <Text style={styles.callerStatus}>Incoming Call</Text>
      <Text style={styles.number}>Unknown Number</Text>
      <Text style={styles.location}>India | Potential Spam Scan Active</Text>

      {/* Accept / Reject Buttons */}
      <View style={styles.buttonRow}>
        
        <View style={styles.buttonWrapper}>
          <TouchableOpacity 
            style={[styles.actionBtn, styles.rejectBtn]} 
            onPress={() => router.back()}
          >
            <PhoneOff color="white" size={30} />
          </TouchableOpacity>
          <Text style={styles.btnLabel}>Decline</Text>
        </View>

        <View style={styles.buttonWrapper}>
          <TouchableOpacity 
            style={[styles.actionBtn, styles.acceptBtn]} 
            onPress={() => router.push("/monitoring")}
          >
            <PhoneIncoming color="white" size={30} />
          </TouchableOpacity>
          <Text style={styles.btnLabel}>Accept</Text>
        </View>

      </View>

    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", padding: 20 },
  callerIconContainer: { alignItems: 'center', justifyContent: 'center', marginBottom: 30 },
  iconCircle: { width: 120, height: 120, borderRadius: 60, backgroundColor: 'rgba(255,255,255,0.1)', justifyContent: 'center', alignItems: 'center', borderWidth: 1, borderColor: 'rgba(255,255,255,0.2)' },
  pulse: { position: 'absolute', width: 120, height: 120, borderRadius: 60, backgroundColor: '#00f2ff' },
  callerStatus: { fontSize: 18, color: "#94a3b8", marginBottom: 5, letterSpacing: 1 },
  number: { fontSize: 32, color: "white", fontWeight: "bold" },
  location: { color: "#00f2ff", marginTop: 10, fontSize: 14, fontWeight: '500' },
  buttonRow: { flexDirection: "row", gap: 60, marginTop: 100, width: '100%', justifyContent: 'center' },
  buttonWrapper: { alignItems: 'center' },
  actionBtn: { width: 75, height: 75, borderRadius: 40, justifyContent: "center", alignItems: "center", elevation: 10, shadowColor: '#000', shadowOpacity: 0.3, shadowRadius: 5 },
  rejectBtn: { backgroundColor: "#ef4444" },
  acceptBtn: { backgroundColor: "#22c55e" },
  btnLabel: { color: 'white', marginTop: 12, fontSize: 14, fontWeight: '500' }
});