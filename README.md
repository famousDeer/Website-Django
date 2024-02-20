# :round_pushpin: General info
It's my first website made with Django framework. It contain simple ToDoList (made with tutorial when I was learning Django) and Travel-Manager (still work in progress). 
- **ToDoList** it is simple todo list where you can create your own list base on current user login, and you can add items to list, mark it done and remove.

- **Travel-Manager** this app is for people who's wanna manage travel by them. App contain map where you can add address, with information about price. You can also add descriptions. As you know many videos on TikTok shows some pro tips, so you can add TikTok link to your manager and watch them whenever you want. When you have address of your points you can make a planner. In planner you can drag your place and drop in table with date when you will go.

# Environment
In `requrements.txt` you can find out all libs you need to run this project. Just simply create env:
```bash
> python3 -m venv .django_website
> source .django_website/bin/activate
> pip install -r requrements.txt
```
Or install packages:
```bash
> pip install -r requirements.txt
```

# Run project
To run project you need to be in `My_website/my_website`. Your dirs should looks like this:
```
├── My_website
   ├── my_website
      ├── main
      ├── my_website
      ├── register
      ├── static
      ├── staticfiles
      ├── tictactoe
      ├── travel_manager
      └── manage.py
   ├── .gitignore
   ├── README.md
   └── requirements.txt
```
If you are in correct dir use this command:

```bash
> python3 manage.py makemigrations
> python3 manage.py migrate
> python3 manage.py runserver
```
When everything is ok you should see this message:
```
System check identified no issues (0 silenced).
February 02, 2024 - 15:57:08
Django version 4.2, using settings 'my_website.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Now you should go to server address which is `http://127.0.0.1:8000/`.

# Future updates
- **Travel-Manager**
    - Add feature in planner to manager time range on any attraction
    - Add feature to change order in planner tables
    - Add tests (Working right now) :bulb:
