SELECT * FROM noc_regions ORDER BY acronym;

SELECT olympians.surname, olympians.firstname, competitor_instance.event_id, olympians.athlete_id
FROM olympians, competitor_instance
WHERE olympians.athlete_id = competitor_instance.olympian_id
AND NOC_id = 'KEN'
ORDER BY olympians.surname;

SELECT DISTINCT olympians.surname, olympians.firstname, events.olympic_event, events.sport, competitor_instance.medal, competitor_instance.age, events.year
FROM olympians, events, competitor_instance
WHERE olympians.athlete_id = 71665
AND competitor_instance.olympian_id = olympians.athlete_id
AND events.id = competitor_instance.event_id
AND competitor_instance.medal != '';

SELECT competitor_instance.NOC_ID, COUNT(*) as "Number of Golds"
FROM competitor_instance
WHERE competitor_instance.medal = 'Gold'
GROUP BY competitor_instance.NOC_id
ORDER BY COUNT(*) DESC;