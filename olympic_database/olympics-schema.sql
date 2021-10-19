CREATE TABLE olympians(
    athlete_id SERIAL,
    firstname text,
    surname text
);
CREATE TABLE games(
    id Serial
    year integer,
    season text,
    city text,
    title text
);
CREATE TABLE events(
    id SERIAL,
    sport text,
    olympic_event text
);
CREATE TABLE games_events(
    game_id integer,
    event_id integer
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
