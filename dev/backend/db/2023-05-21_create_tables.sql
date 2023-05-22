create table users (
  id INTEGER PRIMARY KEY,
  name VARCHAR(40) UNIQUE,
  password VARCHAR(40),
  api_key VARCHAR(40)
);

create table channels (
    id INTEGER PRIMARY KEY,
    name VARCHAR(40) UNIQUE
);

create table messages (
  id INTEGER PRIMARY KEY,
  reply_to INTEGER,
  user_id INTEGER,
  channel_id INTEGER,
  message TEXT,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY(channel_id) REFERENCES channels(id) ON DELETE CASCADE,
  FOREIGN KEY(reply_to) REFERENCES messages(id) ON DELETE CASCADE
);

create table reactions (
  message_id INTEGER,
  user_id INTEGER,
  emoji VARCHAR(40),
  PRIMARY KEY(message_id, user_id, emoji),
  FOREIGN KEY(message_id) REFERENCES messages(id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

create table last_read_messages (
  user_id INTEGER,
  channel_id INTEGER,
  message_id INTEGER,
  PRIMARY KEY(user_id, channel_id),
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY(channel_id) REFERENCES channels(id) ON DELETE CASCADE
);