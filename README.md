<h1>A blog application that you can post blog and set your profile</h1>

# How to run project

## Go to the project path of this project
```console
$ cd /to/your/project_path
```
## Create a virtual environment for it
```python
$ python -m venv venv
```
if you don't know about virtual environment <a href="https://pypi.org/project/virtualenv/">virtualenv</a>

## Run your virtual environment 

### Unix/Linux
```console
$ source venv/bin/activate
```
### Windows
```console
$ .\venv\Scripts\activate
```

## Install dependencies
```console
$ pip install -r requirements.txt
```

## Create database with migrate

```console
$ python manage.py migrate
```

## Run server

```console
$ python manage.py runserver
```

Now you can use blogpage

# Login && Register

 ![register](./media/readmeimg/register.png)
 ![login](./media/readmeimg/login.png)

# Main Page

![main](./media/readmeimg/main.png)

# Create Post

![createpost](./media/readmeimg/createpost.png)

# Post Detail

You can see the details of the post 

![postdetail](./media/readmeimg/postdetail.png)

# Post Delete && Update

![postdelete](./media/readmeimg/postdelete.png)
![postupdate](./media/readmeimg/postupdate.png)
![updatedpost](./media/readmeimg/updatedpost.png)

# Profile

![updateprofile](./media/readmeimg/updateprofile.png)

# Announcements
Only admins can add announcement 

![announcement](./media/readmeimg/announcement.png)

Admins can add announcements in the admin panel

![announcementadmin](./media/readmeimg/announcementadmin.png)

# Latest Posts

Latest posts page shows the last 4 post that created

![latestposts](./media/readmeimg/latestposts.png)

# All Post User

You can see all the post that user posted by clicking it's name 

![allpostuser](./media/readmeimg/allpostuser.png)

# Password Reset

![passwordreset](./media/readmeimg/resetpassword.png)
