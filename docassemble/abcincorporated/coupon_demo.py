from docassemble.base.util import variables_snapshot_connection, get_config, user_info, json
import stripe
import psycopg2
from docassemble.base.util import log
from docassemble.base.util import *

def check_coupon(coupon_code, interview_id):
  stripe.api_key = get_config('stripe secret key')
  coupon = stripe.Coupon.retrieve(coupon_code)
  #log('check_coupon function called with interview_id: ' + str(interview_id))
  if coupon:
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    update_payment_status = "UPDATE payment SET is_paid = 'true' WHERE user_id = %s AND interview_id = %s"
    values = (str(user_info().id), str(interview_id))
    try:
        cur.execute(update_payment_status, values)
        conn.commit()  # Commit the changes to the database
        #log("Executing query: %s" % cur.mogrify(update_payment_status, values))
        conn.close()
        return True
    except Exception as e:
        #log("Error executing query: %s" % e)
        conn.rollback()  # Rollback the transaction in case of an error
        conn.close()
        return False
  else:
    return False