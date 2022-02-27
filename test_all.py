import time
import os

import requests

# SINCE I CHANGED MY SERVER LOCATION FOR EU, I HAD TO USE -EU ON THE URL
# OTHERWISE SOME TIMES IT WOULD THROW A 500 ERROR
# {'errors': [{'detail': 'internal error (reference 01FWK6BHT6YM6KJJ2BS2BZMKB3)', 'status': '500'}]}
# THIS MIGHT NOT BE NEEDED FOR YOUR SETUP
BASE_URL = "https://fly-eu.customer.io/v1/"
LOGIN_URL = "login_email"
# INSERT YOUR ENVIRONMENT ID HERE
ENVIRONMENT_ID = os.environ['YOUR_ENVIRONMENT_ID_HERE']
CUSTOMERS_URL = "environments/" + ENVIRONMENT_ID + "/customers"
SEGMENTS_URL = "environments/" + ENVIRONMENT_ID + "/segments"
# INSERT YOUR ACCESS TOKEN HERE
global token
global headers
# INSERT YOUR EMAIL AND PASSWORD HERE
valid_email = os.environ['YOUR_EMAIL_HERE']
valid_password = os.environ['YOUR_PASSWORD_HERE']


def get_login_token():
    global headers
    global token
    resp = login(valid_email, valid_password)
    token = resp.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}
    return resp


def login(email: str, password: str):
    url = LOGIN_URL
    resp = requests.post(BASE_URL + url, json={"email": email, "password": password})
    return resp


def create_customer(customer_id: str, email: str):
    url = BASE_URL + CUSTOMERS_URL
    resp = requests.post(url,
                         json={"customer": {"attributes": {"id": customer_id, "email": email}}},
                         headers=headers)
    return resp


def get_customer_by_email(email: str):
    url = BASE_URL + CUSTOMERS_URL
    return requests.get(url + "?" + "email=" + email, headers=headers)


def update_customers_id(internal_id: str, newid: str):
    url = BASE_URL + CUSTOMERS_URL + "/" + internal_id
    resp = requests.put(url, json={"customer": {"attributes": {"id": newid}}}, headers=headers)
    return resp


def delete_user_by_internal_id(internal_id: str):
    url = BASE_URL + CUSTOMERS_URL + "/" + internal_id
    resp = requests.delete(url, headers=headers)
    return resp


def create_new_segment_with_name(name: str):
    url = BASE_URL + SEGMENTS_URL
    resp = requests.post(url,
                         json={"segment": {"type": "dynamic", "name": name, "conditions": {"and": [
                             {"event": {"name": "*", "filters": {}, "type": "sent_email"}, "times": 1, "within": 0,
                              "inverse": "false"}]}, "description": "seg1desc", "tag_ids": ["3"]}},
                         headers=headers)
    return resp


def get_segment_by_id(id: str):
    url = BASE_URL + SEGMENTS_URL + "/" + id
    return requests.get(url, headers=headers)


def delete_segment_by_id(id: str):
    url = BASE_URL + SEGMENTS_URL + "/" + id
    return requests.delete(url, headers=headers)


def update_segments_name_by_id(s_id: str, name: str):
    url = BASE_URL + SEGMENTS_URL + "/" + s_id
    return requests.put(url, json={"segment": {"type": "dynamic", "name": name, "conditions": {"and": [
        {"event": {"name": "*", "filters": {}, "type": "sent_email"}, "times": 1, "within": 0,
         "inverse": "false"}]}, "description": "seg1desc", "tag_ids": ["3"]}},
                        headers=headers)


def test_login_successful():
    assert "access_token" in get_login_token().json()


def test_login_fail_email_wrong_format():
    resp = login("asfdssf", "asfasfasdf")
    assert resp.status_code == 422
    assert resp.json()['errors'][0]['detail'] == "email must be a valid email address"


def test_login_fail_missing_email():
    resp = login("", "asdasda")
    assert resp.status_code == 422
    assert resp.json()['errors'][0]['detail'] == "email must be a valid email address"


def test_login_fail_missing_password():
    resp = login("asfdssf@fmai.com", "")
    assert resp.status_code == 422
    assert resp.json()['errors'][0]['detail'] == "password must be a non-empty string"


def test_login_fail_wrong_credentials():
    resp = login("asfdssf@gmail.com", "asfasfasdf")
    assert resp.status_code == 401
    assert resp.json()['errors'][0]['detail'] == "unauthorized"


def test_create_customer_successful_with_email_only():
    customer_id = str(time.time())
    assert create_customer("", customer_id + "@gmail.com").status_code == 202
    # had to put this sleep because calling the get on the api to get
    # the customer would return an empty json without the wait
    time.sleep(1)
    resp = get_customer_by_email(customer_id + "@gmail.com")
    assert resp.json()['customers'][0]['attributes']['email'] == customer_id + "@gmail.com"


def test_create_customer_successful_with_email_and_id():
    customer_id = str(time.time())
    assert create_customer(customer_id, customer_id + "@gmail.com").status_code == 202
    # had to put this sleep because calling the get on the api to get
    # the customer would return an empty json without the wait
    time.sleep(1)
    resp = get_customer_by_email(customer_id + "@gmail.com")
    assert resp.json()['customers'][0]['attributes']['email'] == customer_id + "@gmail.com"
    assert resp.json()['customers'][0]['attributes']['id'] == customer_id


def test_create_customer_fail_same_id():
    customer_id = str(time.time_ns())
    assert create_customer("oldid" + customer_id, customer_id + "@gmail.com").status_code == 202
    time.sleep(1)
    assert create_customer("oldid" + customer_id, customer_id + "@gmail.com").status_code == 422


def test_update_customer():
    customer_id = str(time.time_ns())
    assert create_customer("oldid", customer_id + "@gmail.com").status_code == 202
    time.sleep(1)
    resp = get_customer_by_email(customer_id + "@gmail.com")
    assert resp.json()['customers'][0]['attributes']['email'] == customer_id + "@gmail.com"
    internal_id = resp.json()['customers'][0]['internal_id']
    assert update_customers_id(internal_id, "newid" + customer_id).status_code == 202
    time.sleep(1)
    resp = get_customer_by_email(customer_id + "@gmail.com")
    assert resp.json()['customers'][0]['attributes']['id'] == "newid" + customer_id


def test_update_customer_fail_same_id():
    customer_id = str(time.time_ns())
    customer_id2 = str(time.time_ns() + 1)
    assert create_customer("oldid" + customer_id, customer_id + "@gmail.com").status_code == 202
    assert create_customer("oldid2" + customer_id2, customer_id2 + "@gmail.com").status_code == 202
    time.sleep(1)
    resp = get_customer_by_email(customer_id + "@gmail.com")
    assert resp.json()['customers'][0]['attributes']['email'] == customer_id + "@gmail.com"
    internal_id = resp.json()['customers'][0]['internal_id']
    assert update_customers_id(internal_id, "oldid2" + customer_id2).status_code == 422


def test_create_customer_fail_wrong_email_format():
    customer_id = str(time.time())
    resp = create_customer(customer_id, customer_id)
    assert resp.status_code == 422
    assert resp.json()['errors'][0]['detail'] == "Email is invalid."


def test_delete_customer_successful_with_email_only():
    customer_id = str(time.time())
    assert create_customer("", customer_id + "@gmail.com").status_code == 202
    time.sleep(1)
    resp = get_customer_by_email(customer_id + "@gmail.com")
    assert resp.json()['customers'][0]['attributes']['email'] == customer_id + "@gmail.com"
    internal_id = resp.json()['customers'][0]['id']
    assert delete_user_by_internal_id(internal_id).status_code == 204


def test_create_segment():
    resp = create_new_segment_with_name("name")
    assert resp.status_code == 200
    segment_id = resp.json()['segment']['id']
    assert get_segment_by_id(str(segment_id)).status_code == 200


def test_update_segment():
    resp = create_new_segment_with_name("name")
    assert resp.status_code == 200
    segment_id = resp.json()['segment']['id']
    assert get_segment_by_id(str(segment_id)).status_code == 200
    name_to_update = "updated"
    resp = update_segments_name_by_id(str(segment_id), name_to_update)
    assert resp.status_code == 200
    resp = get_segment_by_id(str(segment_id))
    assert resp.json()["segment"]["name"] == name_to_update


def test_delete_segment():
    resp = create_new_segment_with_name("name")
    assert resp.status_code == 200
    segment_id = resp.json()['segment']['id']
    assert get_segment_by_id(str(segment_id)).status_code == 200
    assert delete_segment_by_id(str(segment_id)).status_code == 204
    assert get_segment_by_id(str(segment_id)).status_code == 404
