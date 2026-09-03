# Quiz Application

## Project Description

This is a simple quiz application made using Python for my assessment. It works completely on the command line. There are two types of users - players and admin. A player can register, login, play quizzes from different categories, see their past result and also check the leaderboard. The admin can login separately and add new questions into any category. All the data (users, questions and results) is saved in JSON files inside the `data` folder so it stays even after you close and reopen the program.

## Features I have implemented

- Player registration and login
- Admin login (separate password)
- Playing a quiz - questions come from a category and get shuffled every time
- Shows result after the quiz with which answers were right/wrong
- Player can check their last result again from the menu
- Leaderboard showing best score of every player (handles ties properly, so if two players have same score they get the same rank)
- Admin can add new question to an existing category, or if the category doesn't exist it gets created automatically
- Checks for duplicate question in the same category before adding
- Validation added for username, password, question text, options and correct answer so you can't just put empty/junk values
- If a data file is missing or gets corrupted, the app shows an error message instead of just crashing

## How to run

1. Don't move the files around, keep everything as it is in the project folder.
2. Open terminal/cmd inside the main project folder.
3. Run this command:
```
python main.py
```
4. It'll show a menu, from there you can register / login as player / login as admin.

## Packages required

I haven't used any external library for this, only built-in Python modules:
- json
- getpass
- random
- copy

So no need to pip install anything, just need Python 3 installed (I used Python 3.13 while making this).

## Known limitations / things I know are not perfect

- Passwords are stored as plain text in users.json, not encrypted or hashed. Ideally should be hashed but I haven't added that yet.
- No forgot password option, if someone forgets their password there's no way to reset it from the app.
- There's only one fixed admin account and its password is hardcoded, can't add more admins or change the password through the app.
- Can't edit or delete a question once it has been added by admin.
- Can't delete/reset an old quiz attempt once it's saved.
