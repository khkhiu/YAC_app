import React from 'react';
import { StyleSheet } from 'react-native';
import { JournalScreen } from '../../components/journal/JournalScreen';

export default function HomeScreen() {
  return <JournalScreen />;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  }
});
