SELECT * FROM noc_regions ORDER BY acronym;

SELECT olympians.surname, olympians.firstname, olympians_events.NOC_id, olympians.athlete_id
FROM olympians, olympians_events, events
WHERE olympians.athlete_id = olympians_events.olympian_id
AND events.id = olympians_events.event_id 
AND NOC_id = 'KEN'
ORDER BY olympians.surname;

SELECT olympians.surname, olympians.firstname, events.olympic_event, events.sport, events.medal, events.age
FROM olympians, events, olympians_events
WHERE olympians.athlete_id = 71665
AND olympians_events.olympian_id = olympians.athlete_id 
AND events.id = olympians_events.event_id
AND events.medal != '';

SELECT olympians_events.NOC_ID, COUNT(*) as "Number of Golds"
FROM events, olympians_events
WHERE events.id = olympians_events.event_id
AND events.medal = 'Gold'
GROUP BY olympians_events.NOC_id
ORDER BY COUNT(*) DESC;