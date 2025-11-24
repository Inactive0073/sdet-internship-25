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
