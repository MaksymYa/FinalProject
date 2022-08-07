from array import array
import pymysql.cursors
from mysql.connector import Error
from flask import Flask, redirect, render_template, request, session

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'plant',
    }

def db_create(value):
        
    try:
        connection = pymysql.connect(**config)
        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(value)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        print("MySQL connection is closed")        

def db_select(value, param):
        
    try:
        connection = pymysql.connect(**config)
        with connection:
            with connection.cursor() as cursor:
                # Read a single record
                cursor.execute(value, param)
                #result = cursor.fetchone()
                return cursor
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        print("MySQL connection is closed")   

def db_insert(value, param):
        
    try:
        connection = pymysql.connect(**config)
        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(value, param)
                # your changes.
                connection.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        print("MySQL connection is closed") 

def db_delete(value, param):
        
    try:
        connection = pymysql.connect(**config)
        with connection:
            with connection.cursor() as cursor:
                # Delete record
                cursor.execute(value, param)
                # your changes.
                connection.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        print("MySQL connection is closed")  

def db_update(value, param):
        
    try:
        connection = pymysql.connect(**config)
        with connection:
            with connection.cursor() as cursor:
                # Delete record
                cursor.execute(value, param)
                # your changes.
                connection.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        print("MySQL connection is closed")                 