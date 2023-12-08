# Decision Support System

# Analytic Hierarchy Process(AHP)

## How to use

### Setup

instruction below is used for windows

- create venv 
  ```
  python -m venv venv
  ```
- activate venv
  ```
    venv\Scripts\activate
  ```
- install dependencies for flask
  ```
    pip install -r requirements.txt
  ```

## Run 

instruction below is used for windows

- activate venv(if it hasnt active)
  ```
  venv\Scripts\activate
  ```
- run the server
  ```
  python .\algorithm\app.py
  ```

## Test

send post request with 6 int data to /ahp, examole

```json
{
    "all_criterias":[1,2,3,4,5,6]    
}
```