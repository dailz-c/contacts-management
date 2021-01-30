CREATE TABLE IF NOT EXISTS admins (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  f_name TEXT NOT NULL,
  l_name TEXT NOT NULL,
  password TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS contacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  f_name TEXT NOT NULL,
  l_name TEXT NOT NULL,
  subscription_id INTEGER NOT NULL,
  FOREIGN KEY(subscription_id) REFERENCES subscriptions(id)
  UNIQUE(id, subscription_id)
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subscription_name TEXT UNIQUE NOT NULL,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY(owner_id) REFERENCES admins(id)
)