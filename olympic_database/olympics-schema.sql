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
    olympic_event text
);
CREATE TABLE competitor_instance(
    event_id integer, 
    olympian_id integer, 
    sex text,
    age integer,
    height integer,
    mass decimal, 
    NOC_id text, 
    medal text
);
CREATE TABLE olympians_events(
    event_id integer, 
    olympian_id integer,
    NOC_id text

);
CREATE TABLE noc_regions(
    acronym text,
    region text,
    notes text
);
