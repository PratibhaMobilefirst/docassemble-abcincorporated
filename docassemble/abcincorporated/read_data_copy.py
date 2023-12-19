from docassemble.base.util import variables_snapshot_connection,get_config, user_info, json
import psycopg2
from cryptography.fernet import Fernet
from docassemble.base.util import log
from docassemble.base.util import *
interview_id = ''  # Define the global variable


__all__ = ['add','display','encryptStr','decryptStr','dash','display_copy','delete_data','display_payment','display_register_data','add_registered_data','register_data','reg','retrieve_interview_id','update_payment_status']

def encryptStr(textToConvert):
  key = 'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
  fernet = Fernet(key)
  message = bytes(str(textToConvert), 'utf-8')
  encrypted_message = fernet.encrypt(message)
  return encrypted_message.decode()

def decryptStr(textToDecrypt):
  key = 'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='

  # Create a Fernet object using the key
  fernet = Fernet(key)
  decrypted_message = fernet.decrypt(textToDecrypt)
  return decrypted_message.decode()
 

  
def add(da,mainid,is_pay):
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    da1 = json.dumps(da)
    exists_data = display_copy(mainid)
    if len(exists_data) > 0:
      log('main id: ' + mainid)
      log('payment: ' + is_pay)
      sql_update_query = """Update interview set data = %s where user_id = %s and id = %s"""
      cur.execute(sql_update_query, (da1, user_info().id,mainid))
      
     # sql_update_query1 = """Update payment set is_paid = %s where user_id = %s and interview_id = %s"""
     # cur.execute(sql_update_query1, (is_pay, str(user_info().id),mainid))
        
      conn.commit()
      cur.close()
      return ''
    else:
      postgres_insert_query = """ INSERT INTO interview (data, user_id, filename) VALUES (%s,%s,%s) RETURNING id;"""
      record_to_insert = (da1, user_info().id, user_info().filename)
      cur.execute(postgres_insert_query, record_to_insert)
      primary_key_value = cur.fetchone()[0]

      #log('After insert payment: ' + is_pay)
      
     # cur.execute("""SELECT id FROM interview where user_id = %s ORDER BY id DESC LIMIT 1""")
     # last_id = cur.fetchone()[0]
      
      
      cur.execute("SELECT id FROM interview WHERE user_id = %s ORDER BY id DESC LIMIT 1", (user_info().id,))
      last_id = cur.fetchone()[0]
      
      postgres_insert_query_payment = """ INSERT INTO payment (interview_id, user_id, is_paid) VALUES (%s,%s,%s)"""
      record_to_insert_payment = (primary_key_value, user_info().id, 'false')
      cur.execute(postgres_insert_query_payment, record_to_insert_payment)
      
      conn.commit()
      cur.close()
      log('Print Id: ' + str(primary_key_value))
      #Data.set('last_inserted_id', primary_key_value)
      #last_inserted_id = Data.get('last_inserted_id')
      #Individual(extra_fields=DAObject(last_inserted_id=primary_key_value))
      #log('Last ID: ' + last_inserted_id)
      global interview_id
      interview_id = last_id
      return ''
    
    


def retrieve_interview_id():
    global interview_id
    return interview_id
    
    
def display():
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("select data from interview where user_id="+ str(user_info().id) +" and filename='" + user_info().filename + "'")
    results = [record[0] for record in cur.fetchall()]
    conn.close()
    return results

def display_copy(mainid):
    if mainid == 'unknown':
        results = []
        return results
    else:
        conn = variables_snapshot_connection()
        cur = conn.cursor()
        cur.execute("SELECT data FROM interview WHERE id = %s AND user_id = %s AND filename = %s", (mainid, str(user_info().id), user_info().filename))
        results = [record[0] for record in cur.fetchall()]
        conn.close()
        return results


def display_payment(mainid):
    if mainid == 'unknown':
      results = []
      return results
    else:
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select * from payment where interview_id=" + mainid + " and user_id="+ str(user_info().id))
      rows = cur.fetchall()
      results = []
      for row in rows:
        results.append({
        "interview_id": row[1],
        "user_id": row[2],
        "is_paid": row[3]
      })
      conn.close()
      return results
    
def dash():
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("select * from interview where user_id="+ str(user_info().id))
    rows = cur.fetchall()
    results = []
    for row in rows:
      results.append({
        "id": row[0],
        "user_id": row[1],
        "data": row[2],
        "filename": row[3],
        "creation_date": row[4],
        "modified_date": row[5]
      })
    conn.close()
    return results
 
def delete_data(mainid):
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("delete from interview where id=" + mainid)
      msg = 'Record is deleted successfully'
      conn.commit()
      cur.close()
      conn.close()
      return msg
    
def add_registered_data(da,user_id):
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    da1 = json.dumps(da)
    postgres_insert_query = """ INSERT INTO register (data, user_id, filename) VALUES (%s,%s,%s)"""
    record_to_insert = (da1, user_id, 'docassemble.playground3QDRO:registration_page.yml')
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()
    return ""  
  
def display_register_data(mainid):
    if mainid == 'unknown':
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select * from \"user\" where id = " + str(user_info().id))
      rows = cur.fetchall()
      results = []
      for row in rows:
        results.append({
          "email": row[3],
          "first_name": row[6],
          "last_name": row[7],
        })
      conn.close()
      return results
    else:
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select data from interview where id=" + mainid + " and user_id="+ str(user_info().id)   +" and filename='" + user_info().filename + "'")
      results = [record[0] for record in cur.fetchall()]
      conn.close()
      return results

def register_data():
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  cur.execute("select data from register where user_id="+ str(user_info().id) )
  results = [record[0] for record in cur.fetchall()]
  conn.close()
  return results

def reg():
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  cur.execute("select data from register where user_id="+ str(user_info().id) )
  results = [record[0] for record in cur.fetchall()]
  conn.close()
  return results

def update_payment_status(interview_id):
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  update_payment_status = "UPDATE payment SET is_paid = 'true' WHERE user_id = %s AND interview_id = %s"
  values = (str(user_info().id), str(interview_id))
  try:
      cur.execute(update_payment_status, values)
      conn.commit()  # Commit the changes to the database
      log("Executing query: %s" % cur.mogrify(update_payment_status, values))
      conn.close()
      return True
  except Exception as e:
      log("Error executing query: %s" % e)
      conn.rollback()  # Rollback the transaction in case of an error
      conn.close()
      return False