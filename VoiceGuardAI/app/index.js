import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { MotiView } from 'moti';

export default function ProtectionScreen() {
  const [isScam, setIsScam] = useState(false);

  return (
    <View style={[styles.container, { backgroundColor: isScam ? '#2a0000' : '#000814' }]}>
      
      {/* Dynamic AI Waveform - 3 layers */}
      <View style={styles.waveContainer}>
        {[1, 1.5, 2].map((scale, index) => (
          <MotiView
            key={index}
            from={{ scale: 1, opacity: 0.6 }}
            animate={{ scale: scale + 0.5, opacity: 0 }}
            transition={{ loop: true, duration: 1500 + (index * 500), type: 'timing' }}
            style={[styles.pulse, { borderColor: isScam ? '#ff4d4d' : '#00f2ff' }]}
          />
        ))}
        <View style={[styles.core, { backgroundColor: isScam ? '#ff0000' : '#00f2ff' }]} />
      </View>
      
      <Text style={[styles.statusText, { color: isScam ? '#ff4d4d' : '#00f2ff' }]}>
        {isScam ? "⚠️ HIGH RISK SCAM DETECTED" : "SHIELD ACTIVE: MONITORING..."}
      </Text>

      <View style={styles.transcriptBox}>
        <Text style={styles.infoLabel}>LIVE TRANSCRIPT</Text>
        <Text style={styles.transcriptText}>
          {isScam ? "[SCAMMER]: '...Aapka account block ho jayega, turant OTP dein!'" : "[CALLER]: 'Hello, how can I help you today?'"}
        </Text>
      </View>

      <TouchableOpacity 
        style={[styles.button, { backgroundColor: isScam ? '#ff0000' : '#1a1a1a' }]} 
        onPress={() => setIsScam(!isScam)}
      >
        <Text style={styles.buttonText}>{isScam ? "DISCONNECT CALL" : "STOP SCANNING"}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  waveContainer: { height: 200, justifyContent: 'center', alignItems: 'center' },
  pulse: { width: 120, height: 120, borderRadius: 60, borderWidth: 2, position: 'absolute' },
  core: { width: 40, height: 40, borderRadius: 20, shadowBlur: 20, shadowColor: '#00f2ff', shadowOpacity: 0.8 },
  statusText: { fontSize: 18, fontWeight: '900', marginTop: 40, textAlign: 'center', letterSpacing: 1 },
  transcriptBox: { padding: 15, backgroundColor: 'rgba(255,255,255,0.05)', marginTop: 40, borderRadius: 12, width: '100%', borderWidth: 1, borderColor: 'rgba(255,255,255,0.1)' },
  infoLabel: { color: '#666', fontSize: 10, marginBottom: 5, fontWeight: 'bold' },
  transcriptText: { color: '#fff', fontSize: 14, fontStyle: 'italic', lineHeight: 20 },
  button: { marginTop: 60, paddingVertical: 15, paddingHorizontal: 40, borderRadius: 30, borderWidth: 1, borderColor: 'rgba(255,255,255,0.2)' },
  buttonText: { color: 'white', fontWeight: 'bold', fontSize: 14 }
});