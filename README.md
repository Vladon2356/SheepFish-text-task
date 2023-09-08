## Setup 

1. Clone the repository:
    ```sh
    $ git clone https://github.com/Vladon2356/SheepFish-text-task.git
    ```
2. Populate env.example env.celery.example and end.db.example files and rename it on .env .celery.example and .env.db
3. Build and run containers with command:
    ```sh
    $ make build_containers
    ```
4. After step 3 populate the database with command:
    ```sh
    $ make populate_db
    ```
5. Create superuser (username-admin, password-admin) with command:
    ```sh
    $ make create_superuser
    ```
## To get started
By url http://0.0.0.0:8000/swagger/ there is swagger doc.

## Order create json examples
this field are required in order create json:
- point_id 
- order_number - unique order number

```json
{
    "meet": 1,
    "apple": 1,
    "potato": 1,
    "point_id": 4,
    "order_number": "19"
}
```
```json
{
   "fish": 5,
   "rice": 3,
   "point_id": 1,
   "order_number": "d361e30bd5174bf7a00e1e9611b8f38c"
}
```
