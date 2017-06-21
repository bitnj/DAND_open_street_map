SELECT COUNT(*)
FROM (SELECT uid FROM nodes
UNION
SELECT uid FROM ways) as users;