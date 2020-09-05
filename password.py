# Function to check for valid password
def test_password(input_password):

    if " " in input_password:
        return False

    return True