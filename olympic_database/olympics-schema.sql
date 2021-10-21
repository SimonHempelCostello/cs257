CREATE TABLE olympians(
    athlete_id SERIAL,
    firstname text,
    surname text
);
CREATE TABLE games(
    id Integer,
    year integer,
    season text,
    city text,
    title text
);
CREATE TABLE events(
    id SERIAL,
    game_id Integer,
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
CREATE TABLE noc_regions(
    NOC_id text,
    region text,
    notes text
);
