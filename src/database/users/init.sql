CREATE TABLE users
(
    user_name       VARCHAR NOT NULL,
    hashed_password TEXT NOT NULL,
    email           VARCHAR,
    full_name       VARCHAR,
    descriptions    TEXT,
    active          BOOLEAN NOT NULL,
    apps            VARCHAR[],
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

ALTER TABLE users OWNER TO love_and_marriage;

CREATE UNIQUE INDEX users_username_uindex
    ON users (user_name);

INSERT INTO public.users (user_name, hashed_password, email, full_name, descriptions, active, apps, created_at,
                          updated_at)
VALUES ('johndoe'::varchar, '$2b$12$04..e6Se2hkiXWEQOOSJROyIbn5XU4Jw0inYbMBIA1KaWaEwzALLS'::text, 'fake@email'::varchar,
        null::varchar, 'service user'::text, true::boolean, '{"data_transmitter"}', DEFAULT, DEFAULT);