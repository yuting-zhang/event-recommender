DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS checkboxes;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE checkboxes (
	id INTEGER NOT NULL,
	ai INTEGER NOT NULL DEFAULT 0,
  ml INTEGER NOT NULL DEFAULT 0,
	big_data INTEGER NOT NULL DEFAULT 0,
  algos INTEGER NOT NULL DEFAULT 0,
  ar_vr INTEGER NOT NULL DEFAULT 0,
  graphics INTEGER NOT NULL DEFAULT 0,
  bio INTEGER NOT NULL DEFAULT 0,
  linguistics INTEGER NOT NULL DEFAULT 0,
  stats INTEGER NOT NULL DEFAULT 0,
  math INTEGER NOT NULL DEFAULT 0,
  econ INTEGER NOT NULL DEFAULT 0,
	FOREIGN KEY (id) REFERENCES user (id)
);