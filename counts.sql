DROP TABLE IF EXISTS horoscope_counts;

CREATE TABLE horoscope_counts(
    h_text TEXT,
    h_count INT
);

INSERT INTO horoscope_counts (h_text, h_count)
SELECT h_text, COUNT(*) as h_count
FROM horoscopes
GROUP BY h_text;

SELECT h_count as count, COUNT(*) as occurrence
FROM horoscope_counts
GROUP BY h_count
ORDER BY h_count DESC
