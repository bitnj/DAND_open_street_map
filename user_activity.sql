SELECT user, COUNT(*) as cnt
FROM
	((SELECT n.user FROM open_street_map.nodes n
		JOIN
			(SELECT id FROM open_street_map.nodes
				UNION ALL
			SELECT id FROM open_street_map.nodes_tags) AS na
		ON n.id = na.id)
	UNION ALL
	(SELECT w.user FROM open_street_map.ways w
		JOIN
			(SELECT id FROM open_street_map.ways
				UNION ALL
			SELECT id FROM open_street_map.ways_nodes
				UNION ALL
			SELECT id FROM open_street_map.ways_tags) AS wa
		ON w.id = wa.id))
	AS all_activity
GROUP BY user
ORDER BY cnt DESC
LIMIT 10;