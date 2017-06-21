SELECT `key`, `value`, type, COUNT(*) as cnt
FROM open_street_map.nodes_tags
GROUP BY `key`, `value`, type
ORDER BY cnt DESC
LIMIT 10;