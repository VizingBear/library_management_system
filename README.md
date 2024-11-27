# Background information

Need to develop a console application to manage a library of books. The application should allow adding, deleting, searching and displaying books using only standard python 3 libraries

## Project opening

Clone the project

```bash
https://github.com/VizingBear/library_management_system.git
```

Open project directory and create config.py in the project folder (nano example)

```bash
nano config.py
```

Enter any arbitrary text in config.py
The project implements an authorization example, and this text is used to hash the password. The idea was to wall the user who works with the data
```bash
HASH_PASS='random text'
```
Start the application
```bash
python main.py
```

## Usage
When authorizing, use 
```python
login:admin
password:admin
```
Use the console and the appropriate keys to manage the project. Simply press the desired number when a number is required or text when no number is required. The main menu looks like this
```python
Add book(1), Delete book(2), Search book(3), Change book status(4), Exit(0)
```
The database will be created automatically
