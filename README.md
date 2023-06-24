# Social network

A simple Social network based on Python/Django framework;
**Daneshkar** *Python/Django* bootcamp.
***
**How does it works?**
In this social network:
- Each user has a profile with username, password, image and a short bio.
- Each user can view other users profile and follow them.
- Each user can post contents containing title, text content, some images and tags.
- Each user can reply to posts and other replies in a nested manner. User can like or dislike posts and replies.
- Each user can follow a specific tag as well.
- Each user can archive his/her own posts or profile. Other users can not access to archived posts or users.
- Before signing in, each user can only view posts and search usernames.
***
**How to use?**
1. First make a directory:  
```mkdir socialnetwork```
2. Open created directory:  
```cd socialnetwork```
3. Create virtual environment in created directory:  
```python3 -m venv venv```
4. Use venv python intrepeter:  
```source ./venv/bin/activate```
5. Install prerequities:  
```pip install -r requirements.txt```
6. Clone project in `socialnetwork` directory:  
```git clone git@github.com:saraeygh/social-network.git```
6. Use `makemigrations` and `migrate` commands to create database schema and `createsuperuser` command to create admin user. Now you can access social network admin panel with admin user on your localhost:  
```python3 manage.py runserver```
***
## Models designed based on below ERD
![social-network-erd](erd.jpg)