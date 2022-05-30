# Core


- ## [ACCOUNT APP]

  This is Custom user account model that includes the required user information for authentication.

  - ## models.py
    This uses django ORM to interract with the database
        - `username feild`: This field gets the user name
        - `password feild` : This holds the password field


- ## API ENDPOINTS - 
  - [in-bound-sms](https://sms-micro-service.herokuapp.com/api/v1/inbound/sms/)
  - [out-bound-sms](https://sms-micro-service.herokuapp.com/api/v1/outbound/sms/)


- ## ADMIN DATABASE MANAGEMENT PORTAL - 
  - [Micro service admin](https://sms-micro-service.herokuapp.com/admin/)
    - username: any username from the sql dump data
    - password: any password from the sql dump data


- ## Important information
    - `from`:  parameter was changed to `from_`: this is because 'from' is a special reserved word in python
