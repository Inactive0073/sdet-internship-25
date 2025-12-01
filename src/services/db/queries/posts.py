# Все поля WordPress, которые реально важны для тестирования

GET_POST_BY_ID = """
SELECT 
    ID,
    post_title,
    post_content,
    post_status,
    post_name,
    post_author,
    post_date,
    post_modified
FROM wp_posts
WHERE ID = %s;
"""

CHECK_POST_EXISTS = """
SELECT COUNT(*) AS total
FROM wp_posts
WHERE ID = %s;
"""

DELETE_POST_BY_ID = """
DELETE FROM wp_posts
WHERE ID = %s;
"""

UPDATE_POST_TITLE = """
UPDATE wp_posts
SET post_title = %s
WHERE ID = %s;
"""

GET_POST_STATUS = """
SELECT post_status 
FROM wp_posts
WHERE ID = %s;
"""

COUNT_NON_TRASH_POSTS = """
SELECT COUNT(*) AS cnt FROM wp_posts WHERE post_status != 'trash';
"""

GET_ALL_POSTS = """
SELECT *
FROM wp_posts;
"""

CREATE_POST_DB = """
INSERT INTO wp_posts (
    post_author,
    post_date,
    post_date_gmt,
    post_content,
    post_title,
    post_status,
    post_name,
    post_modified,
    post_modified_gmt,
    post_type,
    post_excerpt,
    to_ping,
    pinged,
    post_content_filtered
)
VALUES (
    %s, NOW(), NOW(),
    %s,
    %s,
    %s,
    %s,
    NOW(), NOW(),
    'post',
    '',
    '',
    '',
    ''
);
"""
