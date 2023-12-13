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
    
    "all_criterias":[3,9,3,3,6,6],
    "criteria_length":6,
    "alternatifs_point_per_criterias":[
        // nilai per kriteria per alternatif
    
    [1,6,1,3,1,1],
    [3,9,3,3,1,1],
    [6,6,1,3,1,1],
    [3,6,3,1,1,1],
    [3,3,3,1,1,1],
    [3,6,1,1,1,1],
    [3,9,3,1,1,1],
    [6,6,1,3,1,1],
    [3,6,3,3,1,1],
    [3,9,1,3,1,1],
    [6,9,3,3,1,1],
    [3,9,3,3,1,1],
    [6,6,1,3,1,1],
    [3,3,3,3,1,1],
    [3,1,1,1,1,1]
    ]
}
```