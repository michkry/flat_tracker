CREATE TABLE email_config (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	sender_email VARCHAR(100) NOT NULL,
	sender_email_pass VARCHAR(100) NOT NULL,
	notif_email VARCHAR(100) NOT NULL
);

CREATE TABLE req_time_ctl (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	last_req_date DATE NOT NULL
);

CREATE TABLE url (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	url_alias VARCHAR(500) NOT NULL,
	url TEXT NOT NULL,
	first_req_done INTEGER
);

CREATE TABLE flat (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	flat_id VARCHAR(50) NOT NULL,
	url_id INTEGER NOT NULL,
	announcement_date DATE,
	href TEXT NOT NULL,
	title VARCHAR(500) NOT NULL,
	price NUMBER(10, 2) NOT NULL,
	email_status INTEGER NOT NULL,
	CONSTRAINT fk_flat_url FOREIGN KEY (url_id) REFERENCES url(id)
);
