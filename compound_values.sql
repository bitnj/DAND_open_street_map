SELECT `value`, COUNT(*) as cnt
FROM nodes_tags
WHERE `value` REGEXP '^[a-z][a-z]:[A-Za-z]*'
GROUP BY `value`
ORDER BY cnt DESC;