SELECT w.user, COUNT(*) as cnt
FROM open_street_map.ways w
JOIN
	(SELECT id
	FROM open_street_map.ways
	UNION ALL
	SELECT id
	FROM open_street_map.ways_nodes) AS wa
ON w.id = wa.id
GROUP BY w.user
ORDER BY cnt DESC;