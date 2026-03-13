-- Category Ranking Queries
-- These queries are intended to be run against a database table 'youtube_videos' which contains the cleaned dataset.

-- 1. Top Performing Categories by Total Views
SELECT 
    category_id,
    COUNT(DISTINCT video_id) as num_videos,
    SUM(views) as total_views,
    SUM(likes) as total_likes,
    SUM(dislikes) as total_dislikes
FROM 
    youtube_videos
GROUP BY 
    category_id
ORDER BY 
    total_views DESC;

-- 2. Highest Engagement Rate Categories
-- Engagement = (Likes + Dislikes + Comments) / Views
SELECT 
    category_id,
    SUM(views) as total_views,
    CAST(SUM(likes + dislikes + comment_count) AS FLOAT) / NULLIF(SUM(views), 0) as engagement_rate
FROM 
    youtube_videos
GROUP BY 
    category_id
HAVING 
    SUM(views) > 1000000 -- Filter out low view categories
ORDER BY 
    engagement_rate DESC;

-- 3. Region Comparison: Most Viewed Category per Country
WITH CategoryRanks AS (
    SELECT 
        country,
        category_id,
        SUM(views) as total_views,
        ROW_NUMBER() OVER(PARTITION BY country ORDER BY SUM(views) DESC) as rank
    FROM 
        youtube_videos
    GROUP BY 
        country, category_id
)
SELECT 
    country,
    category_id,
    total_views
FROM 
    CategoryRanks
WHERE 
    rank = 1;
