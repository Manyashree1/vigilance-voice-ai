import { useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { Audio } from "expo-av";
import { MotiView } from 'moti';
import { LinearGradient } from 'expo-linear-gradient';

export default function Monitoring() {
  const [recording, setRecording] = useState<any>(null);
  const [status, setStatus] = useState("Waiting...");
  const [result, setResult] = useState<any>(null);
  const [isListening, setIsListening] = useState(false);

  async function startRecording() {
    const permission = await Audio.requestPermissionsAsync();
    if (!permission.granted) return;
    await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });

    const { recording } = await Audio.Recording.createAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
    setRecording(recording);
    setStatus("Listening...");
    setIsListening(true);
  }

  async function stopRecording() {
    setIsListening(false);
    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();
    setStatus("Sending to AI...");

    const formData = new FormData();
    formData.append("file", { uri, name: "audio.m4a", type: "audio/m4a" } as any);

    try {
      const response = await fetch("http://192.168.1.109:8000/verify-call", {
        method: "POST",
        body: formData,
        headers: { "Content-Type": "multipart/form-data" },
      });
      const data = await response.json();
      setResult(data);
      setStatus("Analysis complete");
    } catch (error) {
      setStatus("AI connection failed");
    }
  }

  return (
    <LinearGradient colors={['#001d3d', '#000814']} style={styles.container}>
      <Text style={styles.title}>AI Monitoring</Text>
      <Text style={[styles.status, { color: isListening ? '#00f2ff' : '#facc15' }]}>{status}</Text>

      {/* Cyber Waveform Animation */}
      <View style={styles.waveContainer}>
        {[...Array(12)].map((_, i) => (
          <MotiView
            key={i}
            from={{ height: 10 }}
            animate={{ height: isListening ? Math.random() * 80 + 20 : 10 }}
            transition={{ type: 'timing', duration: 400, loop: true, delay: i * 50 }}
            style={[styles.waveBar, { backgroundColor: result?.risk_level === 'HIGH' ? '#ff4d4d' : '#00f2ff' }]}
          />
        ))}
      </View>

      <View style={styles.controls}>
        {!isListening ? (
          <TouchableOpacity style={styles.startBtn} onPress={startRecording}>
            <Text style={styles.text}>Start Listening</Text>
          </TouchableOpacity>
        ) : (
          <TouchableOpacity style={styles.stopBtn} onPress={stopRecording}>
            <Text style={styles.text}>Stop & Analyze</Text>
          </TouchableOpacity>
        )}
      </View>

      {result && (
        <View style={styles.resultBox}>
          <Text style={[styles.analysis, { color: result.risk_level === 'HIGH' ? '#ff4d4d' : '#00ffaa' }]}>
            {result.analysis}
          </Text>
          <Text style={styles.details}>Confidence: {result.confidence}%</Text>
          <Text style={styles.details}>Risk: {result.risk_level}</Text>
        </View>
      )}
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", padding: 20 },
  title: { fontSize: 28, color: "white", fontWeight: 'bold', marginBottom: 10 },
  status: { fontSize: 18, marginBottom: 40 },
  waveContainer: { flexDirection: 'row', gap: 6, height: 120, alignItems: 'center' },
  waveBar: { width: 6, borderRadius: 3 },
  controls: { marginTop: 60, width: '100%', alignItems: 'center' },
  startBtn: { backgroundColor: "#00ffaa", padding: 18, borderRadius: 30, width: '80%', alignItems: 'center' },
  stopBtn: { backgroundColor: "#ff4d4d", padding: 18, borderRadius: 30, width: '80%', alignItems: 'center' },
  text: { color: "black", fontWeight: "bold", fontSize: 16 },
  resultBox: { marginTop: 40, padding: 20, backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: 15, width: '100%' },
  analysis: { fontSize: 20, fontWeight: "bold", textAlign: 'center' },
  details: { color: "#94a3b8", marginTop: 5, textAlign: 'center' }
});