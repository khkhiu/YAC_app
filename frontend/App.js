import React, { useState, useEffect } from 'react';
import { SafeAreaView, Text, Button, TextInput, View } from 'react-native';

// Replace with your backend URL
const BACKEND_URL = 'http://10.0.2.2:3000';

export default function App() {
  const [challenge, setChallenge] = useState(null);
  const [response, setResponse] = useState('');

  useEffect(() => {
    fetch(`${BACKEND_URL}/challenges`)
      .then((res) => res.json())
      .then((data) => setChallenge(data[0])); // Get the first challenge for now
  }, []);

  const handleSubmit = () => {
    fetch(`${BACKEND_URL}/challenges`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: 1,  // You should dynamically manage user IDs
        challenge_type: challenge.challenge_type,
        response,
      }),
    }).then(() => {
      alert('Challenge response saved!');
    });
  };

  return (
    <SafeAreaView>
      {challenge ? (
        <View>
          <Text>{challenge.text}</Text>
          <TextInput
            value={response}
            onChangeText={setResponse}
            placeholder="Your response"
          />
          <Button title="Submit" onPress={handleSubmit} />
        </View>
      ) : (
        <Text>Loading challenge...</Text>
      )}
    </SafeAreaView>
  );
}
