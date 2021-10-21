SELECT * FROM noc_regions ORDER BY NOC_id;

SELECT DISTINCT olympians.surname, olympians.firstname, olympians.athlete_id
FROM olympians, competitor_instance
WHERE olympians.athlete_id = competitor_instance.olympian_id
AND NOC_id = 'KEN'
ORDER BY olympians.surname;

SELECT olympians.surname, olympians.firstname, events.olympic_event, events.sport, competitor_instance.medal, competitor_instance.age, games.year
FROM olympians, events, competitor_instance, games
WHERE olympians.athlete_id = 71665
AND competitor_instance.olympian_id = olympians.athlete_id
AND events.id = competitor_instance.event_id
AND events.game_id = games.id
AND competitor_instance.medal != '';

-- This will only present those countries which have at least one medal
SELECT competitor_instance.NOC_ID, COUNT(*) as "Number of Golds"
FROM competitor_instance
WHERE competitor_instance.medal = 'Gold'
GROUP BY competitor_instance.NOC_id
ORDER BY COUNT(*) DESC; 