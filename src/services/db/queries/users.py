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

CREATE_USER = """
INSERT INTO wp_users (user_login, user_pass, user_email, user_nicename, display_name, user_registered)
VALUES (%s, %s, %s, %s, %s, NOW());
"""

CREATE_USER_META_CAP = """
INSERT INTO wp_usermeta (user_id, meta_key, meta_value)
VALUES (%s, 'wp_capabilities', 'a:1:{s:10:"subscriber";b:1;}');
"""

CREATE_USER_META_LEVEL = """
INSERT INTO wp_usermeta (user_id, meta_key, meta_value)
VALUES (%s, 'wp_user_level', '0');
"""
