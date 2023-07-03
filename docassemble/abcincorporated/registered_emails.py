from docassemble.base.util import variables_snapshot_connection,get_config, user_info, json
import psycopg2

__all__ = ['registered_user']

def registered_user():
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("select email from public.user")
    results = [record[0] for record in cur.fetchall()]
    conn.close()
    return results