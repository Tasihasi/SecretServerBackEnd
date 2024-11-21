# Secret Server Backend 
This is a simple Flask application for securely storing and retrieving secrets with an expiration mechanism. 
The secrets are stored with a unique hash, and you can specify a retrieval count (number of allowed views) and an expiration time (in minutes).

### The frontend: https://github.com/Tasihasi/SecretServer/tree/gh-pages

## Features

**Store Secrets:** Store a secret with a specific retrieval count and expiration time.

**Retrieve Secrets:** Retrieve a secret using the generated hash. After the secret is viewed, its retrieval count is decreased.

**Hash Management:** Each secret is associated with a unique hash to ensure secure retrieval.

**Expiration:** Secrets can expire after a specified time, and retrieval will be restricted once the count is exhausted.


## Requirements

  Python 3.x,  
  Flask,  
  Flask-SQLAlchemy,  
  Flask-Cors,  
  A PostgreSQL (or other SQL-compatible) database

# Routes

## POST /secret

This endpoint is used to create a new secret.

**Request Payload (JSON):** 

      {
        "secretText": "My secret message",
        "retrievalCount": 5,
        "expiryDate": 60
      }

**secretText:** The secret message you want to store.
**retrievalCount:** The number of times the secret can be retrieved.
**expiryDate:** The expiration time in minutes for the secret.

**Response:**
    Success: Status Code: 200
    
      {
        "Hash": "generated_hash_string"
      }

  Error (Invalid input): Status Code: 405

    {
    "Error": "Invalid input"
    }

## GET /secret/ < hash_code >
This endpoint is used to retrieve a secret by its unique hash.

**Request URL: GET /secret/< hash >**

< hash > : The unique hash of the secret you want to retrieve.

**Response:**
    Success: Status Code: 200

    {
    "secret": "My secret message"
    }

  Error (Invalid input): Status Code: 200

    {
      "Error": "Error retrieving secret."
    }


# Structure

## flask_app.py
The main entry point of the Flask application.

Initializes the app, configures it, and sets up routes.

## config.py
Contains application configuration, such as database URI, secret key, and any other settings required.

## models.py

Contains the PostData and GetData classes.
### PostData: 
  Used to create a new secret, handle hash generation, expiration, and database insertion.

  Public function: 
  **post_to_db()** -> Returns an bool
  
### GetData:
  Used to retrieve a secret using its unique hash.

  Public function: 
  **get_secret( hash : str)** -> Returns Flask response object => Can be returned immediately in the route.

Contains methods for interacting with the database, such as adding new secrets and retrieving them by hash.

## routes.py

Contains the route definitions for the app:

**/secret:** To save a secret.

**/secret/< hash >:** To retrieve a secret.

## Is_valid_request.py

It contains the **is_valid_request** function, which ensures that the request is valid (i.e., it includes the necessary data).


# Error Handling

The application handles errors such as:

Invalid input data when creating a secret.

Errors in retrieving a secret, including cases where the hash does not exist or the retrieval count is exhausted.


    





