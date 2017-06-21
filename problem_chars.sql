SELECT `key`, `value` , type
FROM nodes_tags
WHERE `value` REGEXP '[=\+/&<>;\'\"\?%#$@\,\.\t\r\n]'
GROUP BY `key`, `value`, type
ORDER BY `key`;
