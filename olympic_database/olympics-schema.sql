CREATE TABLE olympians(
    athlete_id SERIAL,
    firstname text,
    surname text
);
CREATE TABLE events(
    id SERIAL,
    title text,
    year integer,
    season text,
    city text,
    sport text,
    olympic_event text,
    medal text,
    sex text,
    age integer,
    height integer,
    mass decimal
);
CREATE TABLE olympians_events(
    event_id integer, 
    olympian_id integer,
    NOC_id text

);
CREATE TABLE NOC(
    acronym text,
    region text,
    notes text
);
