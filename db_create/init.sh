#!/bin/sh
python
create_db.py
u = User(username=${USERNAME}, email=${EMAIL})
u.set_password(${SECRET_SUPER_PASS})
u.check_password(${SECRET_SUPER_PASS})
