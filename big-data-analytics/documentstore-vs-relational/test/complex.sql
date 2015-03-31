SELECT * FROM flickr_pics LIMIT 30;
SELECT timestamp, labels FROM flickr_pics LIMIT 20;
SELECT imgurl, labels FROM flickr_pics WHERE timestamp > 1427735965 AND timestamp < 1427735988 LIMIT 30;
SELECT COUNT(DISTINCT blogurl) FROM flickr_pics;

