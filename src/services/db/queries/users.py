GET_USER_BY_ID = """
SELECT 
    ID,
    user_login,
    user_email,
    user_registered,
    user_status
FROM wp_users
WHERE ID = %s;
"""

CHECK_USER_BY_EMAIL = """
SELECT COUNT(*) AS total
FROM wp_users
WHERE user_email = %s;
"""

DELETE_USER_BY_ID = """
DELETE FROM wp_users
WHERE ID = %s;
"""
