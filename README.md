# Customer.io test

## Notes
###Confusing test description
From the test description: 

“Profiles: Create a new profile, update a new profile, and delete that profile (in the UI you can do this by navigating to "People" from the left-side navigation).” 

* There’s no mention of profiles on the UI
* The API is “/customers”
####The names should be the same everywhere?

I know naming conventions can be complicated, especially taking into account API/UI changes 

## Steps
1. First I took the urls and parameters from Chrome’s devtools
2. Then used postman to make sure it’s working
3. Then moved to code
* I would have used cypress for the tests but assumed from the test description they were API tests.

If I have time I’ll try to do them using cypress.
* The test took me A LONG TIME to finish (20+ hours).

I wish I had more time to do negative test cases to cover expected failures


## Bugs found
* When I use the url without the server parameter (fly-eu), I get a 500 error
{'errors': [{'detail': 'internal error (reference 01FWK6BHT6YM6KJJ2BS2BZMKB3)', 'status': '500'}]}

When I was creating my account I changed the server since I'm in Europe.  
When some tests started failing randomly I noticed the difference in the URL in the network tab.  
https://fly-eu.customer.io/v1/environments/117258/customers/ works but https://fly.customer.io/v1/environments/117258/customers/ doesn’t when doing a post call to create a customer.  
Not sure there should be a redirect automatically.  
* I was able to get a success call when trying to create a user with no id and no email, both on the frontend (by getting the selector of the confirm button and clicking it using javascript) and on the API tests
https://share.getcloudapp.com/NQux6erA


## Installation instructions
0. (optional step if you don’t have any python environment setup either with pycharm or in the terminal)  
Install PyCharm
1. Make sure you have python 3.9 as an interpreter on pycharm or installed on the terminal
2. Install the requests and pytest package.  
Run “pip install -r requirements.txt” in the terminal
3. Get the bearer token from the cookie “_access” after login on the platform (if you don’t have an account, create one)  
On the code, on line 16, insert that token   
On line 19 and 20 insert your email and password  
4. On the left side of the UI, click People.   
Then copy the number on the URL between “env/” and “/people”
https://fly.customer.io/env/COPYTHISNUMBER/people  
On the code, on line 12, insert that number




