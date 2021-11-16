##Gemini Test Automation for Order Placement API's: New Order

Docs: https://docs.gemini.com/rest-api/#new-order

Requirements/Solution:
- Please code up a suite of functional test cases in the language of your choice
- Include both positive and negative cases
- Be able to quantify the number of distinct tests run
- You may consume other API endpoints to aid in your testing, but do not attempt
   to test any other API endpoints (e.g., order status). The objective here is to rigorously 
  test this one endpoint as thoroughly as you can.
- Clearly articulate your assumption

#### Setup project:
    
    pip install -r requirement.txt

#### Running Tests:
First change-directory into tests folder

    cd ../path/to/gemini-api-automation/tests

Run all tests
    
    python3 -m pytest
    
Run positive test cases (37/58 Test Cases):

    python3 -m pytest -v -m positive

Run negative test cases (21/58 Test Cases)

    python3 -m pytest -v -m negative
    
    

#### Possible Bugs Found
1. Using invalid or empty X-GEMINI-APIKEY and valid X-GEMINI-SIGNATURE returns InvalidSignature
2. Using integer values for New Order optional parameters min_amount, stop_price, account returns status code 200
3. Using float values for New Order optional parameters min_amount, stop_price, account returns status code 200
4. Using negative values for New Order optional parameters min_amount, stop_price, account returns status code 200 

