CREATE OR REPLACE PROCEDURE create_user(username VARCHAR(50), password VARCHAR(255))
LANGUAGE SQL
AS $$
INSERT INTO users (username, password)
VALUES (username, password);
$$;

CREATE OR REPLACE FUNCTION get_user_by_username(username VARCHAR(50))
RETURNS TABLE (id INTEGER, username VARCHAR(50), password VARCHAR(255))
AS $$
SELECT id, username, password FROM users WHERE username = $1;
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_token_by_token(token VARCHAR(255))
RETURNS TABLE (id INTEGER, user_id INTEGER, created_at TIMESTAMP, expires_at TIMESTAMP)
AS $$
SELECT id, user_id, created_at, expires_at FROM tokens WHERE token = $1;
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION create_token(user_id INTEGER, token VARCHAR(255), expires_at TIMESTAMP)
RETURNS TABLE (id INTEGER, user_id INTEGER, token VARCHAR(255), created_at TIMESTAMP, expires_at TIMESTAMP)
AS $$
INSERT INTO tokens (user_id, token, expires_at)
VALUES (user_id, token, expires_at)
RETURNING id, user_id, token, created_at, expires_at;
$$ LANGUAGE sql;

CREATE OR REPLACE PROCEDURE delete_token(user_id INTEGER, token VARCHAR(255))
LANGUAGE SQL
AS $$
DELETE FROM tokens WHERE user_id = $1 AND token = $2;
$$;

CREATE OR REPLACE PROCEDURE create_task_list(name VARCHAR(100), user_id INTEGER)
LANGUAGE SQL
AS $$
INSERT INTO task_lists (name, user_id)
VALUES (name, user_id);
$$;

CREATE OR REPLACE FUNCTION get_task_lists_by_user_id(user_id INTEGER)
RETURNS TABLE (id INTEGER, name VARCHAR(100), user_id INTEGER)
AS $$
SELECT id, name, user_id FROM task_lists WHERE user_id = $1;
$$ LANGUAGE sql;

CREATE OR REPLACE PROCEDURE delete_task_list(task_list_id INTEGER)
LANGUAGE SQL
AS $$
DELETE FROM task_lists WHERE id = task_list_id;
$$;

CREATE OR REPLACE PROCEDURE create_task(title TEXT, list_id INTEGER)
LANGUAGE SQL
AS $$
INSERT INTO tasks (title, list_id)
VALUES (title, list_id);
$$;

CREATE OR REPLACE PROCEDURE update_task(task_id INTEGER, title TEXT, completed BOOLEAN)
LANGUAGE SQL
AS $$
UPDATE tasks SET title = title, completed = completed
WHERE id = task_id;
$$;

CREATE OR REPLACE PROCEDURE delete_task(task_id INTEGER)
LANGUAGE SQL
AS $$
DELETE FROM tasks WHERE id = task_id;
$$;
