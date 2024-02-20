from docassemble.base.util import variables_snapshot_connection,get_config, user_info, json, get_config
import psycopg2
from cryptography.fernet import Fernet
from docassemble.base.util import log
from docassemble.base.util import *
interview_id = ''  # Define the global variable
which_user = ''

__all__ = ['add','display','encryptStr','decryptStr','dash','display_copy','delete_data','display_payment','display_register_data','add_registered_data','add_registered_data1','register_data','reg','retrieve_interview_id','update_payment_status','update_profile','update_profile1','display_register_data_j','courts','plans','court_address','claimant','add_to_joinder','reuse_data','add_interview_type','display_type_of_interview','edit_interview_type','file_name','reuse_from_diff_interview','display_qdro_intake_data_copy','add_to_qdro_intake','address_of_admin_and_sponsor','qdro_intake_new_users','reuse_intake_data','reuse_from_intake_interview','qdro_intake_user_id','qdro_intake_user_information','qdro_intake_user_name_details','username','use_intake_button','reuse_button_info', 'delete_button_info','delete_previous_button_info','display_plan1','get_plan_type']    

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


def add(da, mainid, is_pay, type_of_interview):
    global interview_id
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    da1 = json.dumps(da)
    exists_data = display_copy(mainid)
    
    if type_of_interview == 'reuse' and len(exists_data) > 0:
        # Insert a new row into the interview table without specifying the id
        postgres_insert_query = """INSERT INTO interview (data, user_id, filename) VALUES (%s, %s, %s) RETURNING id;"""
        record_to_insert = (da1, user_info().id, user_info().filename)
        cur.execute(postgres_insert_query, record_to_insert)
        new_primary_key_value = cur.fetchone()[0]
        conn.commit()

        # Insert a new row into the payment table for the new interview ID
        postgres_insert_query_payment = """INSERT INTO payment (interview_id, user_id, is_paid) VALUES (%s, %s, %s);"""
        record_to_insert_payment = (new_primary_key_value, user_info().id, 'false')
        cur.execute(postgres_insert_query_payment, record_to_insert_payment)
        conn.commit()

        cur.close()
        interview_id = new_primary_key_value
        return ''
    else:
        if mainid != 'unknown':
            if len(exists_data) > 0:
                #log('main id: ' + mainid)
                #log('payment: ' + is_pay)
                # Update the existing row with the same ID
                sql_update_query = """UPDATE interview SET data = %s WHERE user_id = %s AND id = %s"""
                cur.execute(sql_update_query, (da1, user_info().id, mainid))
                primary_key_value = mainid
            else:
                # Insert a new row into the interview table with the provided ID
                postgres_insert_query = """INSERT INTO interview (data, user_id, filename) VALUES (%s, %s, %s) RETURNING id;"""
                record_to_insert = (da1, user_info().id, user_info().filename)
                cur.execute(postgres_insert_query, record_to_insert)
                primary_key_value = cur.fetchone()[0]
                log('After insert payment: ' + is_pay)
                
                # Insert a new row into the payment table for the new interview ID
                postgres_insert_query_payment = """INSERT INTO payment (interview_id, user_id, is_paid) VALUES (%s, %s, %s);"""
                record_to_insert_payment = (primary_key_value, user_info().id, 'false')
                cur.execute(postgres_insert_query_payment, record_to_insert_payment)
                conn.commit()

            conn.commit()
            cur.close()
            #log('Print Id: ' + str(primary_key_value))
            interview_id = primary_key_value
            return ''
        else:
            # Handle the case when mainid is 'unknown'
            # Insert a new row into the interview table without specifying the id
            postgres_insert_query = """INSERT INTO interview (data, user_id, filename) VALUES (%s, %s, %s) RETURNING id;"""
            record_to_insert = (da1, user_info().id, user_info().filename)
            cur.execute(postgres_insert_query, record_to_insert)
            primary_key_value = cur.fetchone()[0]
            log('After insert payment: ' + is_pay)
            
            # Insert a new row into the payment table for the new interview ID
            postgres_insert_query_payment = """INSERT INTO payment (interview_id, user_id, is_paid) VALUES (%s, %s, %s);"""
            record_to_insert_payment = (primary_key_value, user_info().id, 'false')
            cur.execute(postgres_insert_query_payment, record_to_insert_payment)
            conn.commit()

            conn.commit()
            cur.close()
            #log('Print Id: ' + str(primary_key_value))
            interview_id = primary_key_value
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
    if mainid == 'unknown' or not mainid:
      results = []
      return results
    else:
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("SELECT data FROM interview WHERE id = %s AND user_id = %s", (mainid, str(user_info().id)))
      results = [record[0] for record in cur.fetchall()]
      conn.close()
      return results

def display_payment(mainid):
    if mainid == 'unknown' or not mainid:
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
    cur.execute("select * from interview where user_id="+ str(user_info().id) + "ORDER BY id DESC")
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

def reuse_data(mainid):
    if mainid == 'unknown' or not mainid:
      results = []
      return results
    else:
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("SELECT data FROM interview WHERE id ="+str(mainid) + " and user_id="+ str(user_info().id)+" and filename='" + user_info().filename+"'")
      result = cur.fetchone()
      conn.close()
      print(result)
      r={'f_name':result[0]['f_name'],'l_name':result[0]['l_name'],'email_id':result[0]['email_id'],'final_judgment':result[0]['final_judgment'],'judgment_date':result[0]['judgment_date'],'judgment_deal':result[0]['judgment_deal'],'is_same_date':result[0]['is_same_date'],'petition_dom':result[0]['petition_dom'],'petition_dos':result[0]['petition_dos'],'response_dom':result[0]['response_dom'],'response_dos':result[0]['response_dos'],'petitioner_field':result[0]['petitioner_field'],'respondent_field':result[0]['respondent_field']}
      return r
#reuse1    
    
def add_registered_data1(da,user_id):
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    da1 = json.dumps(da)
    postgres_insert_query = """ INSERT INTO register (data, user_id, filename) VALUES (%s,%s,%s)"""
    record_to_insert = (da1, user_id, user_info().filename)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()
    return "" 

def add_registered_data(da):
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    da1 = json.dumps(da)
    postgres_insert_query = """
        INSERT INTO register (data, user_id, filename)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE
        SET data = register.data || excluded.data
    """
    record_to_insert = (da1, user_info().id, user_info().filename)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()
    return ""

def update_profile(da):
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    da1 = json.dumps(da)
    exists_data = reg()
    if len(exists_data) > 0:
        sql_update_query = """UPDATE register SET data = %s WHERE user_id = %s"""
        cur.execute(sql_update_query, (da1, user_info().id))
        conn.commit()
        cur.close()
        return ''
    else:
        return ''
    
def update_profile1(da):
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    sql_update_query = "Update public.user set first_name = %s, last_name = %s where id = %s"
    result = cur.execute(sql_update_query, (da['user.name.first'], da['user.name.last'], user_info().id))
    conn.commit()
    cur.close()
    return ''
  


  
def display_register_data(mainid):
    if mainid == 'unknown' or not mainid:
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
  values = (str(user_info().id), str(interview_id))
  
  currStatus =  cur.execute( "select is_paid from payment WHERE user_id = %s AND interview_id = %s",values)
  
  if currStatus and currStatus.is_paid == true:
    return False
  
  update_payment_status = "UPDATE payment SET is_paid = 'true' WHERE user_id = %s AND interview_id = %s"
  try:
      cur.execute(update_payment_status, values)
      conn.commit()  # Commit the changes to the database
      log("Executing query: %s" % cur.mogrify(update_payment_status, values))
      conn.close()
      return True
  except Exception as e:
      #log("Error executing query: %s" % e)
      conn.rollback()  # Rollback the transaction in case of an error
      conn.close()
      return False
    
def display_register_data_j():
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
    
    
def courts():
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  store_court = cur.execute("select display_sort_for_courts from courts")
  results = [record[0] for record in cur.fetchall()]
  conn.close()
  return results

def court_address(court_name):
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("SELECT * FROM courts WHERE display_sort_for_courts = '" + court_name + "'")
      rows = cur.fetchall()
      results = []
      for row in rows:
        results.append({
          "count_court_district": row[2],
          "court_address_line1": row[5],
          "court_address_line2": row[6],
        })
      conn.close()
      return results


def plans():
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  cur.execute("select dplan_name from retirement_plan")
  results = [record[0] for record in cur.fetchall()]
  conn.close()
  return results

def claimant(pick_plan):
    if not pick_plan:  # Check if pick_plan is empty
        return ''  # Return an empty string if pick_plan is empty

    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("SELECT mplan_name FROM retirement_plan WHERE dplan_name = %s", (pick_plan,))
    result = cur.fetchone()  # Fetch a single record

    # Add the new query
    cur.execute("SELECT mplan_address_line1, mplan_address_line2 FROM retirement_plan WHERE dplan_name = %s", (pick_plan,))
    rows = cur.fetchall()
    results = []
    for row in rows:
        if len(row) >= 2:  # Check if the row has enough elements
            results.append({
                "mplan_address_line1": row[0],
                "mplan_address_line2": row[1],
            })

    conn.close()

    if result:
        return result[0], results  # Return the first column value of the fetched record and the new query results
    else:
        return '', results

def add_to_joinder(data, mainid, type_of_interview):
    global interview_id
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    dump_data = json.dumps(data)
    exists_data = display_copy(mainid)
    if mainid == 'unknown' or not mainid:  # Check if mainid is "unknown"
        # Create a new row without specifying the "id" column
        postgres_insert_query = """INSERT INTO interview (data, user_id, filename) VALUES (%s, %s, %s) RETURNING id;"""
        record_to_insert = (dump_data, user_info().id, user_info().filename)
        cur.execute(postgres_insert_query, record_to_insert)
        primary_key_value = cur.fetchone()[0]
    elif len(exists_data) > 0:
        #log('main id: ' + mainid)
        if type_of_interview == 'reuse':
            # Create a new row without specifying the "id" column
            postgres_insert_query = """INSERT INTO interview (data, user_id, filename) VALUES (%s, %s, %s) RETURNING id;"""
            record_to_insert = (dump_data, user_info().id, user_info().filename)
            cur.execute(postgres_insert_query, record_to_insert)
            primary_key_value = cur.fetchone()[0]
        else:
            # Update the existing row
            sql_update_query = """UPDATE interview SET data = %s WHERE user_id = %s AND id = %s"""
            cur.execute(sql_update_query, (dump_data, user_info().id, mainid))
            primary_key_value = mainid

    else:
        #log('No id: ' + mainid)
        # Insert a new row with the provided ID
        postgres_insert_query = """INSERT INTO interview (data, user_id, filename) VALUES (%s, %s, %s) RETURNING id;"""
        record_to_insert = (dump_data, user_info().id, user_info().filename)
        cur.execute(postgres_insert_query, record_to_insert)
        primary_key_value = cur.fetchone()[0]

    conn.commit()
    cur.close()

    interview_id = primary_key_value
    return ''

def add_interview_type(mainid, file, type_of_interview):
    global interview_id
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    exists_data = display_type_of_interview(mainid)
    if len(exists_data) > 0:
        log('main id: ' + str(mainid))
        sql_update_query = """Update interview_type set type_of_interview = %s where user_id = %s and id = %s"""
        cur.execute(sql_update_query, (type_of_interview, user_info().id, mainid))
        conn.commit()
        cur.close()
        interview_id = mainid
        return ''
    else:
        conn = variables_snapshot_connection()
        cur = conn.cursor()
        postgres_insert_query = """ INSERT INTO interview_type (id, user_id, type_of_interview) VALUES (%s,%s,%s)"""
        record_to_insert = (mainid, user_info().id, type_of_interview)
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        cur.close()
        return ""
    
def display_type_of_interview(mainid):
    if mainid == 'unknown' or not mainid:
      results = []
      return results
    else:
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select * from interview_type where id ="+str(mainid) + " and user_id="+ str(user_info().id))
      results = [record for record in cur.fetchall()]
      conn.close()
      return results
def edit_interview_type(mainid,file):
    global interview_id
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    exists_data = display_type_of_interview(mainid)
    if len(exists_data) > 0:
      #log('main id: ' + str(mainid))
      sql_update_query = """Update interview_type set type_of_interview = %s where user_id = %s and id = %s"""
      cur.execute(sql_update_query, ('edit', user_info().id,mainid))
      conn.commit()
      cur.close()
      interview_id = mainid
      if file[0]=='docassemble.playground3QDRO:joinder_generator.yml' or file[0]=='docassemble.playground3:joinder_generator.yml':
        command('leave',url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:joinder_generator.yml&id='+str(mainid)+'&new_session=1')
      elif file[0]=='docassemble.playground3QDRO:adverse.yml' or file[0]=='docassemble.playground3:adverse.yml':
        command('leave',url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:adverse.yml&id='+str(mainid)+'&new_session=1')
      elif file[0]=='docassemble.playground3:Government_Plan_DRO.yml' or file[0]=='docassemble.playground3QDRO:Government_Plan_DRO.yml':
        command('leave',url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:Government_Plan_DRO.yml&id='+str(mainid)+'&new_session=1')
      else:
        command('leave',url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:qdro.yml&id='+str(mainid)+'&new_session=1')
      return ''
    else:
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      postgres_insert_query = """ INSERT INTO interview_type (id, user_id, type_of_interview) VALUES (%s,%s,%s)"""
      record_to_insert = (mainid, user_info().id, 'edit')
      cur.execute(postgres_insert_query, record_to_insert)
      conn.commit()
      cur.close()
      if file[0]=='docassemble.playground3:joinder_generator.yml' or file[0]=='docassemble.playground3QDRO:joinder_generator.yml':
        command('leave',url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:joinder_generator.yml&id='+str(mainid)+'&new_session=1')
      elif file[0]=='docassemble.playground3:adverse.yml' or file[0]=='docassemble.playground3QDRO:adverse.yml':
        command('leave',url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:adverse.yml&id='+str(mainid)+'&new_session=1')
      elif file[0]=='docassemble.playground3:Government_Plan_DRO.yml' or file[0]=='docassemble.playground3QDRO:Government_Plan_DRO.yml':
        command('leave',url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:Government_Plan_DRO.yml&id='+str(mainid)+'&new_session=1')
      else:
        command('leave',url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:qdro.yml&id='+str(mainid)+'&new_session=1')
      return "" 
def file_name(mainid):
    if mainid == 'unknown' or not mainid:
      results = []
      return results
    else:
      global interview_id
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select filename from interview where id=" + str(mainid) + " and user_id="+ str(user_info().id))
      results = [record[0] for record in cur.fetchall()]
      conn.close()
      return results
    
def reuse_from_diff_interview(which_doc, type_of_interview):
    if type_of_interview == 'reuse' and which_doc == 'Joinder':
        command('leave', url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:joinder_generator.yml&id=' + str(retrieve_interview_id()) + '&new_session=1')
    elif type_of_interview == 'reuse' and which_doc == 'QDRO':
        command('leave', url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:qdro.yml&id=' + str(retrieve_interview_id()) + '&new_session=1')
    elif type_of_interview == 'reuse' and which_doc == 'Notice of Adverse Interest':
        command('leave', url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:adverse.yml&id=' + str(retrieve_interview_id()) + '&new_session=1')
    elif type_of_interview == 'reuse' and which_doc == 'Government Plan DRO':
        command('leave', url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:Government_Plan_DRO.yml&id=' + str(retrieve_interview_id()) + '&new_session=1')
   
def display_qdro_intake_data_copy(mainid):
    if mainid == 'unknown' or not mainid:
      results = []
      return results
    else:
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select data from qdro_intake_new where id=" + mainid)
      results = [record[0] for record in cur.fetchall()]
      conn.close()
      return results
  
def add_to_qdro_intake(data, mainid, username):
    global interview_id
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    dump_data = json.dumps(data)
    exists_data = display_qdro_intake_data_copy(mainid)
    if mainid == 'unknown' or not mainid:  # Check if mainid is "unknown"
        # Create a new row without specifying the "id" column
        postgres_insert_query = """INSERT INTO qdro_intake_new (data, username) VALUES (%s, %s) RETURNING id;"""
        record_to_insert = (dump_data, username)
        cur.execute(postgres_insert_query, record_to_insert)
        result = cur.fetchone()
        if result is not None:
            primary_key_value = result[0]
        else:
            primary_key_value = None
    else:
        log('No id: ' + mainid)
        # Insert a new row with the provided ID
        postgres_insert_query = """INSERT INTO qdro_intake_new (data, username) VALUES (%s, %s) RETURNING id;"""
        record_to_insert = (dump_data, username)
        cur.execute(postgres_insert_query, record_to_insert)
        result = cur.fetchone()
        if result is not None:
            primary_key_value = result[0]
        else:
            primary_key_value = None

    conn.commit()
    cur.close()

    interview_id = primary_key_value
    return ''

  
def address_of_admin_and_sponsor(plan_name):
    conn = variables_snapshot_connection()
    cur = conn.cursor()

    try:
        if plan_name is None:
            return ""
        else:
            query = "SELECT * FROM f5500_sf2021_all WHERE sf_plan_name = %s"
            cur.execute(query, (plan_name,))
            rows = cur.fetchall()

            results = []
            for row in rows:
                result_row = {
                    "date": row[6],
                    "plan_sponsor_name": row[7],
                    "plan_sponsor_address1":row[9],
                    "plan_sponsor_address2":row[10],
                    "plan_sponsor_city": row[11],
                    "plan_sponsor_state": row[12],
                    "plan_sponsor_zip": row[13],
                    "plan_sponsor_phone": row[21],
                    "plan_sponsor_foreign_address1":row[14],
                    "plan_sponsor_foreign_address2":row[15],
                    "plan_sponsor_foreign_city": row[16],
                    "plan_sponsor_foreign_state": row[17],
                    "plan_sponsor_foreign_country": row[18],
                    "plan_sponsor_foreign_zip": row[19],
                    "plan_admin_name": row[23],
                    "plan_admin_address1": row[25],
                    "plan_admin_address2": row[26],
                    "plan_admin_city": row[27],
                    "plan_admin_state": row[28],
                    "plan_admin_zip": row[29],
                    "plan_admin_phone": row[37],
                    "plan_admin_foreign_address1": row[30],
                    "plan_admin_foreign_address2": row[31],
                    "plan_admin_foreign_city": row[32],
                    "plan_admin_foreign_state": row[33],
                    "plan_admin_foreign_country": row[34],
                    "plan_admin_foreign_zip": row[35],
                }
                results.append(result_row)

            return results
    except Exception as e:
        # Log or handle the exception appropriately
        print(f"Error fetching data: {e}")
        return []  # Return an empty list or handle the error case accordingly
    finally:
        cur.close()
        conn.close()
  
  
  
def address_of_admin_and_sponsor(plan_name):
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      if plan_name is None:
        return ""
      else:
        cur.execute("SELECT * FROM f5500_sf2021_all WHERE sf_plan_name = '" + plan_name + "'")
        rows = cur.fetchall()
        results = []
        for row in rows:
          results.append({
            "date": row[6],
            "plan_sponsor_name": row[7],
            "plan_sponsor_address1":row[9],
            "plan_sponsor_address2":row[10],
            "plan_sponsor_city": row[11],
            "plan_sponsor_state": row[12],
            "plan_sponsor_zip": row[13],
            "plan_sponsor_phone": row[21],
            "plan_sponsor_foreign_address1":row[14],
            "plan_sponsor_foreign_address2":row[15],
            "plan_sponsor_foreign_city": row[16],
            "plan_sponsor_foreign_state": row[17],
            "plan_sponsor_foreign_country": row[18],
            "plan_sponsor_foreign_zip": row[19],
            "plan_admin_name": row[23],
            "plan_admin_address1": row[25],
            "plan_admin_address2": row[26],
            "plan_admin_city": row[27],
            "plan_admin_state": row[28],
            "plan_admin_zip": row[29],
            "plan_admin_phone": row[37],
            "plan_admin_foreign_address1": row[30],
            "plan_admin_foreign_address2": row[31],
            "plan_admin_foreign_city": row[32],
            "plan_admin_foreign_state": row[33],
            "plan_admin_foreign_country": row[34],
            "plan_admin_foreign_zip": row[35],
          
          })
        conn.close()
        return results
      
def qdro_intake_new_users():
      conn = variables_snapshot_connection()
      cur = conn.cursor()
      cur.execute("select username from qdro_intake_new")
      results = [record[0] for record in cur.fetchall()]
      conn.close()
      return results
    
def reuse_intake_data(which_user):
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM qdro_intake_new WHERE username = %s", (which_user,))
  rows = cur.fetchall()
  results = []
  for row in rows:
    results.append({
      "id": row[0],
      "data": row[1],
      "creation_date": row[2],
      "modified_date": row[3],
      "username": row[4]
      })
  conn.close()
  return results

def reuse_from_intake_interview(select_interview,which_user):
    if select_interview == 'Joinder':
        command('leave', url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:joinder_generator.yml&username=' + str(which_user) + '&new_session=1')
    elif select_interview == 'Notice of Adverse Interest':
        command('leave', url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:adverse.yml&username='+ str(which_user) + '&new_session=1')
    elif select_interview == 'QDRO':
        command('leave', url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:qdro.yml&username=' + str(which_user) + '&new_session=1')
    elif select_interview == 'Government Plan DRO':
        command('leave', url='https://doc.lexyalgo.com/interview?i=docassemble.playground3QDRO:Government_Plan_DRO.yml&username=' + str(which_user) + '&new_session=1')
    return which_user

def username():
  global which_user
  return which_user

def qdro_intake_user_id(which_user):
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  cur.execute("SELECT id FROM qdro_intake_new WHERE username = %s", (which_user,))
  results = [record[0] for record in cur.fetchall()]
  conn.close()
  return results
  
def qdro_intake_user_information(qdro_intake_id, which_user):
    conn = variables_snapshot_connection()
    cur = conn.cursor()

    # Check if the record already exists
    cur.execute("SELECT COUNT(*) FROM qdro_intake_user_info WHERE qdro_intake_id = %s AND user_name = %s", (qdro_intake_id, which_user))
    count = cur.fetchone()[0]

    if count == 0:
        # If the record doesn't exist, insert a new one
        postgres_insert_query = """INSERT INTO qdro_intake_user_info (qdro_intake_id, user_name) VALUES (%s, %s)"""
        record_to_insert = (qdro_intake_id, which_user)
        cur.execute(postgres_insert_query, record_to_insert)
    else:
        # If the record exists, delete the existing record
        postgres_delete_query = """DELETE FROM qdro_intake_user_info WHERE qdro_intake_id = %s AND user_name = %s"""
        record_to_delete = (qdro_intake_id, which_user)
        cur.execute(postgres_delete_query, record_to_delete)

        # Then, insert the selected user's data at the end
        postgres_insert_query = """INSERT INTO qdro_intake_user_info (qdro_intake_id, user_name) VALUES (%s, %s)"""
        record_to_insert = (qdro_intake_id, which_user)
        cur.execute(postgres_insert_query, record_to_insert)

    conn.commit()
    cur.close()
    return ""
  
def qdro_intake_user_name_details():
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  cur.execute("SELECT user_name FROM qdro_intake_user_info ORDER BY id DESC LIMIT 1")
  results = [record[0] for record in cur.fetchall()]
  conn.close()
  return results
  
def use_intake_button(qdro_intake_id,intake_button):
  
    conn = variables_snapshot_connection()
    cur = conn.cursor()

    # Then, insert the selected user's data at the end
    postgres_insert_query = """INSERT INTO qdro_intake_reuse_button_info (qdro_intake_id, qdro_reuse_button) VALUES (%s, %s)"""
    record_to_insert = (qdro_intake_id, intake_button)
    cur.execute(postgres_insert_query, record_to_insert)

    conn.commit()
    cur.close()
    return ""
  
def reuse_button_info(id):
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM qdro_intake_reuse_button_info where qdro_intake_id ="+ str(id))
  results = [record[0] for record in cur.fetchall()]
  conn.close()
  return results
  
def delete_button_info(qdro_intake_id):
    conn = variables_snapshot_connection()
    cur = conn.cursor()

    # Define the SQL query to delete the row based on qdro_intake_id
    postgres_delete_query = """DELETE FROM qdro_intake_reuse_button_info"""
    
    # Execute the query
    cur.execute(postgres_delete_query, (qdro_intake_id,))

    # Commit the transaction and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()

    return " "
  
def delete_previous_button_info():
    conn = variables_snapshot_connection()
    cur = conn.cursor()

    # Define the SQL query to delete the row with the maximum id
    postgres_delete_query = """
    DELETE FROM qdro_intake_reuse_button_info
    WHERE id = (SELECT MAX(id) FROM qdro_intake_reuse_button_info)
    """
    
    # Execute the query
    cur.execute(postgres_delete_query)

    # Commit the transaction and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()

    return " "


def display_plan1():
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("SELECT distinct sf_plan_name from f5500_sf2021_all where LENGTH(sf_plan_name) >= 3")
    results = [record[0] for record in cur.fetchall()]
    conn.close()
    return results
  
def get_plan_type(plan_name):
    try:
        # Establish a database connection (you mentioned you already have this part)
        conn = variables_snapshot_connection()
        cur = conn.cursor()

        # Define the SQL query with placeholders for the plan name and code
        query = "SELECT sf_plan_name, sf_type_pension_bnft_code FROM f5500_sf2021_all WHERE sf_plan_name = %s"

        # Define the parameters to replace placeholders in the query
        parameters = (plan_name,)

        # Execute the query with the parameters
        cur.execute(query, parameters)

        # Fetch the result
        result = cur.fetchone()

        # Close the cursor and the database connection
        cur.close()
        conn.close()

        # Check if the result is not empty and return the specific text based on sf_type_pension_bnft_code
        if result:
            sf_type_pension_bnft_code = result[1]
            if "2" in sf_type_pension_bnft_code and "1" in sf_type_pension_bnft_code:
                return ''
            if "2" in sf_type_pension_bnft_code:
                return "Deferred Compensation (Cash & Investment Account 401K)"
            elif "1" in sf_type_pension_bnft_code:
                return "Pension Plan (Plans that guarantee monthly retirement income)"
        return None  # Return None if no matching record is found

    except Exception as e:
        # Handle any exceptions that might occur during the database operation
        print("Error:", str(e))
        return None