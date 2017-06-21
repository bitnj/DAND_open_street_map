SELECT n.user, COUNT(*) as cnt
FROM open_street_map.nodes n
JOIN
	(SELECT id
	FROM open_street_map.nodes
	UNION ALL
	SELECT id
	FROM open_street_map.nodes_tags) AS na
ON n.id = na.id
GROUP BY n.user
ORDER BY cnt DESC;