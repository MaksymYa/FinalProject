from db import db_create, db_insert, db_select
import mysql.connector
from mysql.connector import Error
from werkzeug.security import check_password_hash, generate_password_hash

def start_table():
    users = "CREATE TABLE IF NOT EXISTS users (id int NOT NULL AUTO_INCREMENT, first_name varchar(45) NOT NULL, last_name varchar(45) NOT NULL, login varchar(45) NOT NULL, password varchar(150) NOT NULL, id_role int NOT NULL, PRIMARY KEY (`id`), UNIQUE KEY `email_UNIQUE` (`email`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"
    role = "CREATE TABLE IF NOT EXISTS role (id INT NOT NULL AUTO_INCREMENT, role VARCHAR(45) NOT NULL, PRIMARY KEY (`id`), UNIQUE INDEX `role_UNIQUE` (`role` ASC) VISIBLE)"
    customers = "CREATE TABLE IF NOT EXISTS customers (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(45) NOT NULL, email VARCHAR(45) NOT NULL, country VARCHAR(45) NOT NULL, PRIMARY KEY (`id`), UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE, UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);"
    parts = "CREATE TABLE IF NOT EXISTS parts (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(45) NOT NULL, price FLOAT NOT NULL, worcker_price FLOAT NOT NULL, id_counterparty INT NOT NULL, PRIMARY KEY (`id`), UNIQUE INDEX `part_UNIQUE` (`part` ASC) VISIBLE)"
    orders = "CREATE TABLE IF NOT EXISTS orders (id INT NOT NULL AUTO_INCREMENT, id_part INT NOT NULL, amount INT NOT NULL, reg_data DATE NOT NULL, shipping_data DATE NOT NULL, status VARCHAR(45) NOT NULL, PRIMARY KEY (`id`))"
    stock = "CREATE TABLE IF NOT EXISTS stock (id INT NOT NULL AUTO_INCREMENT, id_part INT NOT NULL, amount INT NOT NULL, id_stage INT NOT NULL, PRIMARY KEY (`id`))"
    status = "CREATE TABLE IF NOT EXISTS statuses (id INT NOT NULL AUTO_INCREMENT, status VARCHAR(45) NOT NULL, UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE, UNIQUE INDEX `status_UNIQUE` (`status` ASC) VISIBLE)"
    shift_tasks = "CREATE TABLE IF NOT EXISTS shift_tasks (id INT NOT NULL AUTO_INCREMENT, date DATE NOT NULL, operator_id VARCHAR(45) NOT NULL,  id_part INT NOT NULL, amount_plan int NOT NULL, amount_fact int DEFAULT NULL, id_status int NOT NULL DEFAULT '2', PRIMARY KEY (`id`))"
    stages = "CREATE TABLE IF NOT EXISTS stages (id int NOT NULL AUTO_INCREMENT, stage varchar(45) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"
    salary = "CREATE TABLE IF NOT EXISTS salary (id INT NOT NULL AUTO_INCREMENT, id_user INT NOT NULL, salary double DEFAULT '0', PRIMARY KEY (`id`))"

    #value = "INSERT INTO users (first_name, last_name, email, password, id_role) VALUES (%s, %s, %s, %s, %s)" 
    #hash = generate_password_hash('admin')
    #param = ['Admin', 'Admin', 'admin', hash, '1']
    
    db_create(users)
    db_create(role)
    db_create(customers)
    db_create(parts)
    db_create(orders)
    db_create(stock)
    db_create(status)
    db_create(shift_tasks)
    db_create(stages)
    db_create(salary)
    #db_insert(value, param)
    #print(db_select(value, param))
    
        

