SELECT user, COUNT(*) as cnt
FROM
    ((SELECT n.user FROM nodes n
        JOIN
            (SELECT id FROM nodes
                UNION ALL
            SELECT id FROM nodes_tags) AS na
        ON n.id = na.id)
    UNION ALL
    (SELECT w.user FROM ways w
        JOIN
            (SELECT id FROM ways
                UNION ALL
            SELECT id FROM ways_nodes
                UNION ALL
            SELECT id FROM ways_tags) AS wa
        ON w.id = wa.id))
    AS all_activity
GROUP BY user
ORDER BY cnt DESC
LIMIT 10;