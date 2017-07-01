# django-asterisk
management panel to manage devices connected to Asterisk PBX. 
Those device have no piblic IP-s and we cannot connect to them directly.
This is the reason I used Asterisk Managment Interface (AMI) to send commands to devices.

there was used Djangos internal admin interface to manage database.

## capabilites.
- authentificated users management
- organization management
- devices management.
- generation of config files which are downloaded and applied by devices.
- sending commands to devivces via Asterisks/AMI interface.
- Restfull API with key authentification.

## stack used:
- Resis: messaging subsistem used for asyncronous interaction with AMI interface.
- Django
- SQLite database.

