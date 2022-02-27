# Customer.io test

## Notes
### This was fun!
I actually had a lot of fun (and headaches) doing this test.  
It has been a while since I used python and did any API testing.  
I took advantage of it and learned about github actions as well.  
With github actions I found a [flaky test](https://github.com/jpita/cio-gabriel/actions), it seems the 1 second wait is not enough for the API to return the expected result updated

### Confusing test description
From the test description: 

“Profiles: Create a new profile, update a new profile, and delete that profile (in the UI you can do this by navigating to "People" from the left-side navigation).” 

* There’s no mention of profiles on the UI
* The API is “/customers”
#### The names should be the same everywhere?

I know naming conventions can be complicated, especially taking into account API/UI changes.  

## Steps taken during the test
1. After playing around in the platform, I took the urls and parameters from Chrome’s devtools
2. Then used postman to make sure it’s working
3. Then moved to code
* I would have used cypress for the tests but assumed from the test description they were API tests.

If I have time I’ll try to do them using cypress.
* The test took me A LONG TIME to finish (20+ hours).

I wish I had more time to do negative test cases to cover expected failures


## Bugs found
* When I use the url without the `-eu` server parameter, I get a 500 error
```{'errors': [{'detail': 'internal error (reference 01FWK6BHT6YM6KJJ2BS2BZMKB3)', 'status': '500'}]}```

When I was creating my account I changed the server location since I'm in Europe.  
When some tests started failing randomly I noticed the difference in the URL in the network tab.  
https://fly-eu.customer.io/v1/environments/117258/customers/ works but   
https://fly.customer.io/v1/environments/117258/customers/ doesn’t when doing a post call to create a customer.  
Not sure there should be a redirect automatically.  
* I was able to get a success `200 OK` call when trying to create a user with no id and no email.  


This happened both on the frontend (by getting the selector of the confirm button and clicking it using javascript) and on the API tests.  

Video showing the issue: https://share.getcloudapp.com/NQux6erA


## Installation and execution instructions
0. (optional step if you don’t have any python environment setup either with PyCharm or in the terminal)  
Install PyCharm
1. Make sure you have python 3.9 as an interpreter on pycharm or installed on the terminal
2. Install the requests and pytest package.  
Run `pip install -r requirements.txt` in the terminal
3. Now login on the [customer.io](https://fly.customer.io/login) platform with your account and write down the email and password (if you don’t have an account, create one)  
4. On the left side of the UI, click People.   
Then write down the environment number on the URL between `env/` and `/people`
https://fly.customer.io/env/COPYTHISNUMBER/people
5. Now open the `test_all.py` file on your favorite editor/IDE.  
If you are using PyCharm you should open the folder where the file is present as a new project.
6. On line 13, insert the environment number you got from step 4 replacing this entire text `os.environ['YOUR_ENVIRONMENT_ID_HERE']` with your email (the entire text, not just the big letters) surrounded by "".   
example:  
from `ENVIRONMENT_ID = os.environ['YOUR_ENVIRONMENT_ID_HERE']`   
to `ENVIRONMENT_ID = "2143543"`
7. On line 20 insert your email replacing this entire text `os.environ['YOUR_EMAIL_HERE']` with your email (the entire text, not just the big letters) surrounded by "".   
example:  
from `valid_email = os.environ['YOUR_EMAIL_HERE']`   
to `valid_email = "blabla@gmail.com"`  
8. On line 21 do the same for the password:  
from `valid_password = os.environ['YOUR_PASSWORD_HERE']`     
to `valid_password = "uramazinglysecurepassword"`
9. Save the file
10. Run `pytest` in the terminal and the tests should start running.  
If the tests don't start, try `python -m pytest` , or `python3 -m pytest` and if nothing else works, then install pycharm, install the pytest plugin and run the tests in the UI of the IDE.
