// app/index.tsx
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

export default function HomeScreen() {
  const steps = [
    "Incoming Call",
    'User taps "Protect Call"',
    "App listens in background",
    "AI continuously analyzes voice",
    "Live alert if scam / AI voice detected"
  ];

  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep(prev => (prev + 1 < steps.length ? prev + 1 : prev));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {steps.map((step, index) => (
        <View
          key={index}
          style={[styles.stepContainer, index === currentStep && styles.currentStep]}
        >
          <Text style={styles.stepText}>{step}</Text>
          {index !== steps.length - 1 && <Text style={styles.arrow}>↓</Text>}
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingVertical: 50,
    alignItems: 'center',
    backgroundColor: '#f0f4f8',
    minHeight: '100%',
  },
  stepContainer: {
    backgroundColor: '#e2f0ff',
    padding: 20,
    borderRadius: 12,
    width: '80%',
    alignItems: 'center',
    marginVertical: 10,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 4 },
    shadowRadius: 6,
    elevation: 3,
  },
  currentStep: {
    backgroundColor: '#007bff',
  },
  stepText: {
    fontSize: 18,
    color: '#007bff',
    textAlign: 'center',
  },
  arrow: {
    fontSize: 24,
    color: '#007bff',
    marginTop: 10,
  },
});