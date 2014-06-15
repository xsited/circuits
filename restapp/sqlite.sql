DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS l2vpn;


CREATE TABLE sessions (
    session_id VARCHAR(128) NOT NULL PRIMARY KEY,
    atime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data TEXT
);

CREATE TABLE l2vpn (
    id INTEGER PRIMARY KEY,
    l2vpnid VARCHAR(255) NOT NULL UNIQUE,
    port INTEGER DEFAULT 1194,
    protocol INTEGER DEFAULT 1,
    encapsulationtype INTEGER DEFAULT 2,
    encapsulationvalue TEXT,
    s_mac TEXT,
    s_address TEXT NOT NULL,
    d_mac TEXT,
    d_address TEXT NOT NULL,
    created TIMESTAMP,
    updated TIMESTAMP,
    status BOOLEAN DEFAULT 1
);
