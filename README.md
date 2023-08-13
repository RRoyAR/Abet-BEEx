# AlfabetBEExercise
AlfaBet Backend Exercise


## Kafka Server


1. start zookeeper:
   ```.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties```     
2. Start server: ```.\bin\windows\kafka-server-start.bat .\config\server.properties```    


## Installation
1. Deploy Kafka
make sure to set the environment vaiables related:     
```
KAFKA_BROKER=
TOPIC=
GROUP_ID=
```    
2. Deploy PostgreSQL Database   
make sure to set the environment vaiables related:     
```
POSTGRES_PASSWORD=
```    
3. Deploy Redis
make sure to set the environment vaiables related:     
```
REDIS_URL=
REDIS_PORT=
```    


## PostgreSQL Database

### Products Table

Columns | product_id | product_name | cost 
--- |------------|--------------|------
Example 1| 1          | productA     | 290   
Example 2| 2          | productB     | 210   
Example 3 | 3          | productA     | 190   

### Users Table
Columns | product_id | user_name  | email
--- |------------|------------|------------
Example 1| 1          | Roy Arditi | arditiroy@gmail.com
Example 2| 2          | David S    | 
Example 3 | 3          | Noa R    |  


