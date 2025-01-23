-- Create Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    streak INTEGER DEFAULT 0
);

-- Create Challenges table
CREATE TABLE challenges (
    challenge_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    challenge_type VARCHAR(50),
    response TEXT,
    date_completed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert predefined challenges
CREATE TABLE predefined_challenges (
    challenge_id SERIAL PRIMARY KEY,
    challenge_type VARCHAR(50),
    text TEXT
);

INSERT INTO predefined_challenges (challenge_type, text)
VALUES 
('self-awareness', 'Share a memory that reminds you of your resilience.'),
('self-awareness', 'Reflect on a fear you’ve overcome.'),
('connection', 'Thank someone who has supported you.'),
('connection', 'Send a message to someone you lost touch with.');
