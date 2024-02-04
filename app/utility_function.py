from sqlalchemy  import text 
from .mysql_connection import engine_connect


""" Check the user is exist in the database for the provided where condition """
def checking_user_exists(where_condition , col_name):
    try:
        output = {}
        with engine_connect.connect() as conn:
            sql = text(f"SELECT COUNT({col_name}) FROM users WHERE {where_condition}")
            result = conn.execute(sql)
            count = None
            totalrow = result.rowcount
            if totalrow > 0:
                for row in result:
                    count = row[0]

                output['status']  = "success"  
                output['result']  =  count  

            else:
                output['status']  = "failure"  
                output['message']  =  "Something went wrong while checking User existance " 

    except Exception as e:
        output['status']  = "faiure"   
        output['message']  = f"Exception while cheecking user exists : {e}"   

    return output


""" get the update details from the user_details dictionary """
def get_update_condition(user_details):
    update_con = "" 
    count = 0
    for i , j in user_details.items():
        update_con = update_con + f"{i} = '{j}'"
        count += 1 
        if count != len(user_details.keys()):
            update_con = update_con + ","
    
    return update_con

""" Get the user details from the database for the provided id"""
def get_user_details_by_id(id):
    try:
        output = {}
        with engine_connect.connect() as conn:
            sql = text(f"SELECT * FROM users WHERE id = {id}")
            result = conn.execute(sql)
            
            """ checking the result have rows or not """
            total_rows = result.rowcount
            if total_rows == 1:
                for row in result:
                    user_dict = {}
                    user_dict['id'] = row[0]
                    user_dict['fullname'] = row[1]
                    user_dict['email_id'] = row[2]
                    user_dict['gender'] = row[3]
                    user_dict['dob'] = row[4]
                    user_dict['created_date'] = row[5]

                output['status'] = "success"
                output['result'] = user_dict

    except Exception as e:
        output['status'] = "failure"
        output['message'] = f"Exception while get the details of the user"

    return output

""" Getting the all user details list from the database """
def get_all_user_details():
    try:
        output = {}
        with engine_connect.connect() as conn:
            sql = text("SELECT * FROM users;")
            result = conn.execute(sql)
        
        """ checking the result have rows or not if not display the empty list"""
        total_rows= result.rowcount
        if total_rows > 0:
            list_user =[]
            for row in result:
                user_dict = {}
                user_dict['id'] = row[0]
                user_dict['fullname'] = row[1]
                user_dict['email_id'] = row[2]
                user_dict['gender'] = row[3]
                user_dict['dob'] = row[4]
                user_dict['created_date'] = row[5]
                list_user.append(user_dict)

            output['result'] = list_user
        else:
            output['result'] = []

        output['status'] = "success"

    except Exception as e:
        output['status'] = "failure"
        output['message'] = f"Exception while getting the user data from the database : {e}"
    
    return output

""" Deleteing the user from the database for the provided id """
def delete_user_by_id(id):
    try:
        output = {}
        with engine_connect.connect() as conn:
            sql = text(f"DELETE  FROM users WHERE id = {id}")
            result = conn.execute(sql)
            conn.commit()

            """ checking the result have rows or not """
            totalrows = result.rowcount
            if totalrows == 1 :
                output["status"] =  "success" 
                output["message"] =   "User deleted successfully"

            else:
                output["status"] =  "failure" 
                output["message"] =   "Something went wrong while deleting the user"

    except Exception as e:
        output['status'] = "failure"
        output['message'] = f"Exception while delete the user from the database : {e}"
    
    return output

""" Update the user information in the database for the provided id """
def update_user_by_id(id , update_con):
    try:
        output = {}
        with engine_connect.connect() as conn:
            sql = text(f"UPDATE users SET {update_con} WHERE id = {id}")
            result = conn.execute(sql)
            conn.commit()

            """checking the total row return"""
            total_rows = result.rowcount
            if total_rows > 0:
                output["status"] = "success" 
                output["message"] = "User Details Updated Successfully"

            else:
                output["status"] = "failure" 
                output["message"] = "Something went wrong while updating user details"

    except Exception as e:
        output["status"] = "failure" 
        output['message'] = f"Exception while updating the details into the database : {e}"
    
    return output

"""Add the new user into the database """
def add_new_user_into_db(user_data):
    try:
        output = {}
        with engine_connect.connect() as conn:
            sql = f"insert into users (`fullname` ,`email_id` ,`gender`,`dob` , `created_date`) values ('{user_data['fullname']}' ,'{user_data['email_id']}','{user_data['gender']}','{user_data['dob']}','{user_data['created_date']}')"
            result = conn.execute(text(sql))
            conn.commit()
            print(result.rowcount)

            """checking the total row return"""
            total_rows = result.rowcount
            if total_rows > 0:
                output["status"] = "success" 
                output["message"] = "New User added Successfully"

            else:
                output["status"] = "failure" 
                output["message"] = "Something went wrong while inserting user"

    except Exception as e:
        output["status"] = "failure" 
        output['message'] = f"Exception while insertin new user into database : {e}"

    return output