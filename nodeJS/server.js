/**
 * Node.js server to communicate with the Python Telegram bot service
 * This server will:
 * 1. Serve as a web interface for monitoring
 * 2. Communicate with the Python bot through a REST API
 */

const express = require('express');
const axios = require('axios');
const cron = require('node-cron');
const morgan = require('morgan');
const helmet = require('helmet');
const fs = require('fs');
const path = require('path');

// Create Express app
const app = express();
const PORT = process.env.PORT || 3000;
const BOT_SERVICE_URL = process.env.BOT_SERVICE_URL || 'http://bot:5000';

// Setup logging
const logsDir = path.join(__dirname, 'logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir);
}

const accessLogStream = fs.createWriteStream(
  path.join(logsDir, 'access.log'), 
  { flags: 'a' }
);

// Basic security
app.use(helmet());

// Logging
app.use(morgan('combined', { stream: accessLogStream }));
app.use(morgan('dev'));

// Basic middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Function to check bot status
async function checkBotStatus() {
  try {
    const response = await axios.get(`${BOT_SERVICE_URL}/status`);
    return response.data;
  } catch (error) {
    console.error('Error checking bot status:', error.message);
    return { status: 'error', message: 'Could not connect to bot service' };
  }
}

// Routes
app.get('/', async (req, res) => {
  try {
    const botStatus = await checkBotStatus();
    
    res.json({
      status: 'ok',
      message: 'Telegram Journal Bot Server',
      botStatus
    });
  } catch (error) {
    res.status(500).json({ 
      status: 'error', 
      message: 'Could not check bot status' 
    });
  }
});

// Admin routes
app.post('/admin/start', async (req, res) => {
  try {
    const response = await axios.post(`${BOT_SERVICE_URL}/start`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ 
      status: 'error', 
      message: `Failed to start bot: ${error.message}` 
    });
  }
});

app.post('/admin/stop', async (req, res) => {
  try {
    const response = await axios.post(`${BOT_SERVICE_URL}/stop`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ 
      status: 'error', 
      message: `Failed to stop bot: ${error.message}` 
    });
  }
});

app.get('/admin/status', async (req, res) => {
  try {
    const botStatus = await checkBotStatus();
    res.json(botStatus);
  } catch (error) {
    res.status(500).json({ 
      status: 'error', 
      message: `Failed to get status: ${error.message}` 
    });
  }
});

app.get('/admin/users', async (req, res) => {
  try {
    const response = await axios.get(`${BOT_SERVICE_URL}/users`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ 
      status: 'error', 
      message: `Failed to get users: ${error.message}` 
    });
  }
});

// Schedule a health check every hour
cron.schedule('0 * * * *', async () => {
  console.log('Running hourly health check...');
  try {
    const status = await checkBotStatus();
    if (status.status !== 'running') {
      console.log('Bot is not running, attempting to restart...');
      await axios.post(`${BOT_SERVICE_URL}/start`);
    }
  } catch (error) {
    console.error('Health check failed:', error.message);
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Connecting to bot service at ${BOT_SERVICE_URL}`);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down...');
  process.exit(0);
});