# Function to check for valid text
def test_alpha(input_alpha):

    # Iterate through each character of string
    for i in range(len(input_alpha)):
        
        if input_alpha[i].isalpha() == False:
            return False

    # Return True, if no error found
    return True
