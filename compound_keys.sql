SELECT `key`, COUNT(*) as cnt
FROM nodes_tags
WHERE `key` REGEXP '[A-Za-z]*:[A-Za-z]*'
GROUP BY `key`
ORDER BY cnt DESC;