@echo All FOODIM's data will be deleted. 
@echo If you don't want to, please CTRL+C to exit.
@pause

del db.sqlite3
rmdir /s /q community\__pycache__
rmdir /s /q community\migrations
rmdir /s /q inventory\__pycache__
rmdir /s /q inventory\migrations
rmdir /s /q core\__pycache__
rmdir /s /q homepage\__pycache__
rmdir /s /q homepage\migrations

del /s /q __init__.py

@pause