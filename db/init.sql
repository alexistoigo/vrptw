CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    delivery_deadline TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(id),
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS routes (
    id SERIAL PRIMARY KEY,
    start_location GEOMETRY(Point, 4326),
    end_location GEOMETRY(Point, 4326),
    route_data JSONB
);

CREATE TABLE IF NOT EXISTS route_steps (
    id SERIAL PRIMARY KEY,
    route_id INT REFERENCES routes(id),
    step_index INT,
    client_id INT REFERENCES clients(id)
);
