from .main import app 
from datetime import date
from .utility_function import (checking_user_exists , get_user_details_by_id ,get_all_user_details , delete_user_by_id , 
                               get_update_condition , update_user_by_id , add_new_user_into_db)

@app.get('/get_all_user')
def get_all_users():
    try:
        output = {}
        """ get the all user list from the database """
        user_list_res = get_all_user_details()
        if user_list_res['status'] == "success":
            output['user_details_list'] = user_list_res['result']
        else:
            output['message'] = user_list_res['message']

        output['status'] = user_list_res['status']
        
    except Exception as e:
        output['status'] = "failure"
        output["message"] = f"Exception while fetching the user list : {e}" 
        
    return output

        
@app.get('/get_user_details/{id}')
def get_particluar_user(id:int):
    try:
        output = {}
        """ Taking the id as the where condition and passing that condition to the function and to check the user is exists or not """
        id_where_con = f"id = {id}"
        is_user_exists = checking_user_exists(id_where_con , id)

        """ if the status is success and the result = 1 means user is exists """
        if is_user_exists['status'] == "success":
            if is_user_exists['result'] == 1:
                
                """ get the user details from the database """
                user_res = get_user_details_by_id(id)
                if user_res['status'] == "success":
                    output['user_details'] = user_res['result']
                else:
                    output['message'] = user_res['message']

                output['status'] = user_res['status']

            else:
                output['status'] = "failure"
                output["message"] = f"There is no user for present for the provided id : {id} "

        else:
            """ if there is error messsage in the is_user_exists response """        
            output['status'] = is_user_exists['status']
            output["message"] = is_user_exists['message']


    except Exception as e:
        output['status'] = "failure"
        output["message"] = f"Exception while fetching the user details: {e}"
    
    return output
      

@app.delete('/delete_user/{id}')
def delete_particluar_user(id:int):
    try:
        output = {}
        id_where_con = f"id = {id}"
        is_user_exists = checking_user_exists(id_where_con,id)

        if is_user_exists['status'] == "success":
            if is_user_exists['result'] == 1:

                """ delete the user from the database """
                del_res = delete_user_by_id(id)
                output["status"] = del_res['status']
                output["message"] = del_res['message']

            else:
                output["status"] =  "failure" 
                output["message"] =   "There is no user for present for the provided id"
        
        else:
            output["status"] =  is_user_exists['status']
            output["message"] =  is_user_exists['message']

    except Exception as e:
        output["status"] =  "failure" 
        output["message"]  =  f"Exception while fetching the user details: {e}"
    
    return output


@app.post('/add_new_user')
def insert_user_data(user_data : dict):
    try:
        output ={}

        fullname = user_data.get('fullname' ,'')
        email_id = user_data.get('email_id' ,'')
        gender = user_data.get('gender','')
        dob = user_data.get('dob','')
        created_date = date.today()

        if (fullname == '') or (fullname == None):
            output["status"] = "failure" 
            output["message"] = "Provide the fullname"
            return output
        
        if (email_id == '') or (email_id == None):
            output["status"] = "failure" 
            output["message"] = "Provide the email id"
            return output
        
        ### check that email-id is already exists
        where_con_email = f"email_id = '{email_id}'"
        is_user_exists = checking_user_exists(where_con_email, 'email_id')

        if is_user_exists['status'] == "success":

            if is_user_exists['result'] > 0:
                output["status"] = "failure" 
                output["message"] = f"User already present for this {email_id}"
            
            else:
                """Inserting the data into database """
                insert_data = {
                    "fullname" : fullname ,
                    "email_id" : email_id ,
                    "gender" : gender ,
                    "dob" : dob ,
                    "created_date" : created_date
                }
                add_res = add_new_user_into_db(insert_data)
                output['status'] = add_res['status']
                output['message'] = add_res['message']

        else:
            """ If any exception in the checking_user_exists function """
            output['status'] = is_user_exists['status']
            output['message'] = is_user_exists['message']
     

    except Exception as e:
        output['status'] = "failure"
        output['message'] = f"Exception while inserting the user data : {e}"

    return output

@app.put('/update_user/{id}')
def update_particluar_user(id:int , user_details :dict = {}):
    try:
        output = {}
        id_where_con = f"id = {id}"
        is_user_exists = checking_user_exists(id_where_con , id)

        if is_user_exists['status'] == "success":
            if is_user_exists['result'] == 1:

                """ get the update condition from the provided request dictionary"""
                update_con = get_update_condition(user_details)

                if update_con != "":
                    """update the data inthe database """
                    update_res = update_user_by_id(id , update_con)
                    output["status"] = update_res['status']
                    output["message"] = update_res['message']
                   
                else:
                    output["status"] = "failure" 
                    output["message"] = "No data is Provided for Update"

            else:
                output["status"] = "failure" 
                output["message"] = "There is no user for present for the provided id"
               
        else:
            output["status"] =  is_user_exists['status']
            output["message"] =  is_user_exists['message']


    except Exception as e:
        output["status"] = "failure"
        output["message"] = f"Exception while fetching the updating user details: {e}"

    return output


