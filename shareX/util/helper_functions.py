
def is_username_present(dictionary, username):
    for key in dictionary.keys():
        if dictionary[key]['username'] == username:
            return True
    
    return False    

def validate_password(dict, username, password):
    for key, value in dict.items():
        if dict[key]['password'] == password:
            return True 

    return False


def confirm_password(password,confirmation): 
    """
    Confirm if password submitted by user is correct
    """
    if password == confirmation:
        return True
    
    return False
