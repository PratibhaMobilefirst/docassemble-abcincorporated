from docassemble.base.util import variables_snapshot_connection,get_config, user_info, json
import psycopg2

__all__ = ['display_code','display_plan','check_plan']


def display_code1():
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("select sf_sponsor_name from sponsor ORDER BY id ASC LIMIT 2000")
    results = [record[0] for record in cur.fetchall()]
    conn.close()
    return results

def display_plan(code):
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("SELECT distinct sf_plan_name from plan_main n JOIN sponsor_main s ON n.sponsor_id = s.id where s.sf_sponsor_name = '" + code + "'")
    results = [record[0] for record in cur.fetchall()]
    conn.close()
    return results
  
def display_code(pick_plan):
  if pick_plan == 'Deferred Compensation (Cash & Investment Account 401K)':
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT sf_sponsor_name FROM sponsor_main WHERE sf_type_pension_bnft_code LIKE '%2%' AND LENGTH(sf_sponsor_name) >= 3")
    results = [record[0] for record in cur.fetchall()]
    conn.close()
    return results
  else:
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("select distinct sf_sponsor_name from sponsor_main where sf_type_pension_bnft_code like '%1%' AND LENGTH(sf_sponsor_name) >= 3")
    results = [record[0] for record in cur.fetchall()]
    conn.close()
    return results
  
def check_plan(plan_name):
  return plan_name