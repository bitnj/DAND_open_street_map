select w.user, COUNT(*) as cnt
from open_street_map.ways w JOIN open_street_map.ways_tags wt ON w.id=wt.id
GROUP BY user
ORDER BY cnt DESC;