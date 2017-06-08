CREATE TABLE nodes (
    id BIGINT PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid BIGINT,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE nodes_tags (
    id BIGINT,
    `key` TEXT,
    `value` TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE ways (
    id BIGINT PRIMARY KEY NOT NULL,
    user TEXT,
    uid BIGINT,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);

CREATE TABLE ways_tags (
    id BIGINT NOT NULL,
    `key` TEXT NOT NULL,
    `value` TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);

CREATE TABLE ways_nodes (
    id BIGINT NOT NULL,
    node_id BIGINT NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);
