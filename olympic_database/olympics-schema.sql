CREATE TABLE olympians(
    id SERIAL,
    athlete_id integer,
    firstname text,
    surname text
);
CREATE TABLE event(
    id SERIAL,
    title text,
    year integer,
    season text,
    city text,
    sport text,
    medal text,
    sex text,
    age integer,
    height integer,
    mass integer
);
CREATE TABLE olympian_event(
    olympian_id integer, 
    event_id integer,
    NOC_id integer

);
CREATE TABLE NOC(
    id SERIAL,
    acronym text,
    region text,
    notes text,
);
