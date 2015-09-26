Environment: windows7 or Ubuntu 12, I have tested it under these two environments.
Requirements: a python library: pycrypto

How to install pycrypto:
open the terminal: pip install pycrypto

-----------------------------------------------------------

Usage:
This program mainly contains 3 files: 
1. password_manager.py, the main function.
2. password_result.txt, works as database, records the username, encrypt mode and encrypted password. Initially empty.
3. .master_key, which is invisible normally, contains the master key. Initially empty. The program will automatically generate one when first run the python file.

This is an interactive program.
Open the terminal, go to the directory of password_manager.py, and type in:
python password_manager.py

-----------------------------------------------------------

Now , you can input the username and password, but notice that you have to put a space between them to distinguish them.
For example:
When adding new username and password, you can only choose 3 modes to encryt your pass word: ECB, CTR, CBC.
Add username: test, password: testpassword. Mode: CBC
Add username: aaa, password: bbb. Mode: CTR


All those information will be recorded in password_result.txt when program ended (CTRL+D).

