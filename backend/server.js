const express = require('express');
const app = express();
const client = require('./db');
const cors = require('cors');

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello from the backend!');
});

// Endpoint to get challenges
app.get('/challenges', async (req, res) => {
  const result = await client.query('SELECT * FROM predefined_challenges');
  res.json(result.rows);
});

// Endpoint to save user challenge response
app.post('/challenges', async (req, res) => {
  const { user_id, challenge_type, response } = req.body;
  await client.query(
    'INSERT INTO challenges (user_id, challenge_type, response) VALUES ($1, $2, $3)',
    [user_id, challenge_type, response]
  );
  res.status(201).send('Challenge response saved');
});

app.listen(3000, () => {
  console.log('Backend is running on http://localhost:3000');
});
