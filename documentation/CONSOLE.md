# HolbertonBnB - Console :desktop_computer:
The console is a command line interpreter that allows the manipulation of all classes utilized by HolbertonBnB by making calls on the `storage` object instantiated by [models]().  

[Source code.](https://github.com/iChigozirim/holbertonbnb/blob/master/console.py)
  
## Usage :bicyclist:
The console can be run both interactively and non-interactively. To run the console in non-interactive mode, pip any command(s) into an execution of the file `console.py` at the command line.

```
$ echo "help" | ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

Miscellaneous help topics:
==========================
Amenity  BaseModel  City  Place  Review  State  User

(hbnb)
$
```

Alternatively, to use the HolbertonBnB console in interactive mode, run the file `console.py` by itself:
```
$ ./console.py
```
The console can be run with `storage` intantiated in either `FileStorage` or `DBStorage` mode. `FileStorage` is instantiated by default, but `DBStorage` cn be instantiated like so:
```
$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db ./console.py
```
The console functions identically regardless of the `storage` mode.   

While running in interactive mode, the console displays a prompt for input:
```
 $ ./console.py
(hbnb)
```
To quit the console, enter the command `quit`, or input an EOF signal (`ctrl-D`).
```
 $ ./console.py
(hbnb) quit
.----------------------------.
|  Well, that sure was fun!  |
.----------------------------.
$
```
```
 $ ./console.py
(hbnb) EOF
.----------------------------.
|  Well, that sure was fun!  |
.----------------------------.
$
```

### Console Commands
The HolbertonBnB console supports the following commands:  

**create**
- Usage: `create <class> <param 1 name>=<param 1 value> <param 2 name>=<param 2 value> ...` or `<class>.create(<param 1 name>=<param 1 value> <param 2 name>=<param 2 value> ...)`   

Creates a new instance of a given class. The class' ID is printed and the instance is saved to the file `file.json` when the storage mode is set to `FileStorage`, otherwise it is saved to a MySQL database.
```
$ ./console.py
.----------------------------.
|    Welcome to hbnb CLI!    |
|   for help, input 'help'   |
|   for quit, input 'quit'   |
.----------------------------.
(hbnb) create BaseModel
8d6c301d-8764-4c40-ae6c-00e9c1f6f5ea
(hbnb) 
(hbnb) create State name="Arizona"
aa28674c-409e-41a8-83e7-69ea3f9320a8
(hbnb) 
(hbnb) City.create(name="Douglas")
5b54907b-665d-4769-935a-00df9857bf5e
(hbnb) quit
.----------------------------.
|  Well, that sure was fun!  |
.----------------------------.
$ cat file.json ; echo ""
{"BaseModel.8d6c301d-8764-4c40-ae6c-00e9c1f6f5ea": {"id": "8d6c301d-8764-4c40-ae6c-00e9c1f6f5e
a", "created_at": "2022-10-14T21:49:49.698865", "updated_at": "2022-10-14T21:49:49.698905", "__
class__": "BaseModel"}, "State.aa28674c-409e-41a8-83e7-69ea3f9320a8": {"name": "Arizona", "crea
ted_at": "2022-10-14T21:50:49.296127", "updated_at": "2022-10-14T21:50:49.296246", "id": "aa286
74c-409e-41a8-83e7-69ea3f9320a8", "__class__": "State"}, "City.5b54907b-665d-4769-935a-00df9857
bf5e": {"id": "5b54907b-665d-4769-935a-00df9857bf5e", "created_at": "2022-10-14T21:51:14.717074
", "updated_at": "2022-10-14T21:51:14.717127", "__class__": "City"}}
```
  
**show**
- Usage: `show <class> <id>` or <class>.show(<id>)`  

Prints the string representation of a class instance based on a given id.
```
$ ./console.py
.----------------------------.
|    Welcome to hbnb CLI!    |
|   for help, input 'help'   |
|   for quit, input 'quit'   |
.----------------------------.
(hbnb) create Amenity name="Breakfast"
f244cd7c-bb53-402b-8e6b-c9d09ddf2665
(hbnb) 
(hbnb) show Amenity f244cd7c-bb53-402b-8e6b-c9d09ddf2665 
[Amenity] (f244cd7c-bb53-402b-8e6b-c9d09ddf2665) {'name': 'Breakfast', 'created_at': datetime.dat
etime(2022, 10, 14, 21, 57, 20, 805994), 'updated_at': datetime.datetime(2022, 10, 14, 21, 57, 20,
806185), 'id': 'f244cd7c-bb53-402b-8e6b-c9d09ddf2665'}
(hbnb) 
(hbnb) Amenity.show(f244cd7c-bb53-402b-8e6b-c9d09ddf2665)
[Amenity] (f244cd7c-bb53-402b-8e6b-c9d09ddf2665) {'name': 'Breakfast', 'created_at': datetime.datet
ime(2022, 10, 14, 21, 57, 20, 805994), 'updated_at': datetime.datetime(2022, 10, 14, 21, 57, 20, 80
6185), 'id': 'f244cd7c-bb53-402b-8e6b-c9d09ddf2665'}
(hbnb)
```
    
**destroy**
- Usage: `destroy <class> <id>` or `<class>.destroy(<id>)`  

Deletes a class instance based on a given id.
```
(hbnb) create State name="Alabama"
d7db2f4a-ac10-4632-b90d-381f9685a676
(hbnb) create City name="Babbie"
ff53dd31-b9f2-4de0-8944-96ba713e7753
(hbnb) 
(hbnb) show State d7db2f4a-ac10-4632-b90d-381f9685a676
[State] (d7db2f4a-ac10-4632-b90d-381f9685a676) {'name': 'Alabama', 'created_at': datetime.datetime(202
2, 10, 14, 22, 6, 6, 343879), 'updated_at': datetime.datetime(2022, 10, 14, 22, 6, 6, 344093), 'id': '
d7db2f4a-ac10-4632-b90d-381f9685a676'}
(hbnb) show City ff53dd31-b9f2-4de0-8944-96ba713e7753
[City] (ff53dd31-b9f2-4de0-8944-96ba713e7753) {'name': 'Babbie', 'created_at': datetime.datetime(2022, 
10, 14, 22, 6, 21, 840225), 'updated_at': datetime.datetime(2022, 10, 14, 22, 6, 21, 840279), 'id': 'f
f53dd31-b9f2-4de0-8944-96ba713e7753'}
(hbnb) 
(hbnb) destroy State d7db2f4a-ac10-4632-b90d-381f9685a676
(hbnb) City.destroy(ff53dd31-b9f2-4de0-8944-96ba713e7753)
(hbnb) 
(hbnb) show State d7db2f4a-ac10-4632-b90d-381f9685a676
** no instance found **
(hbnb) show City ff53dd31-b9f2-4de0-8944-96ba713e7753
** no instance found **
(hbnb)
```
  
**all**
- Usage: `all` or `all <class>` or `<class>.all()`  

 Prints the string representations of all instances of a given class. If no class name is provided, the command prints all instances of every class.
```
(hbnb) create Amenity
ac6370b2-b9ba-4e8a-9eb7-bce0b130be73
(hbnb) create Amenity
e1e8193f-0fff-40f1-91a7-8cf13c0564fc
(hbnb) create City name="Tokyo"
c5b5305f-d366-4c44-9dca-9811201eaa9b
(hbnb) create City name="Rio"
3a8a6acd-e9c2-493b-b86d-5cbd64596829
(hbnb) 
(hbnb) all Amenity
[[Amenity] (ac6370b2-b9ba-4e8a-9eb7-bce0b130be73) {'id': 'ac6370b2-b9ba-4e8a-9eb7-bce0b130b
e73', 'created_at': datetime.datetime(2022, 10, 14, 22, 11, 39, 203434), 'updated_at': date
time.datetime(2022, 10, 14, 22, 11, 39, 203487)}, [Amenity] (e1e8193f-0fff-40f1-91a7-8cf13c
0564fc) {'id': 'e1e8193f-0fff-40f1-91a7-8cf13c0564fc', 'created_at': datetime.datetime(2022,
10, 14, 22, 12, 2, 152953), 'updated_at': datetime.datetime(2022, 10, 14, 22, 12, 2, 153014)
}]
(hbnb) 
(hbnb) City.all()
[[City] (c5b5305f-d366-4c44-9dca-9811201eaa9b) {'name': 'Tokyo', 'created_at': datetime.date
time(2022, 10, 14, 22, 12, 44, 868360), 'updated_at': datetime.datetime(2022, 10, 14, 22, 12
, 44, 868484), 'id': 'c5b5305f-d366-4c44-9dca-9811201eaa9b'}, [City] (3a8a6acd-e9c2-493b-b86
d-5cbd64596829) {'name': 'Rio', 'id': '3a8a6acd-e9c2-493b-b86d-5cbd64596829', 'created_at': 
datetime.datetime(2022, 10, 14, 22, 13, 40, 848842), 'updated_at': datetime.datetime(2022, 1
0, 14, 22, 13, 40, 848903)}]
(hbnb) 
(hbnb) all
[[Amenity] (ac6370b2-b9ba-4e8a-9eb7-bce0b130be73) {'id': 'ac6370b2-b9ba-4e8a-9eb7-bce0b130be7
3', 'created_at': datetime.datetime(2022, 10, 14, 22, 11, 39, 203434), 'updated_at': datetime
.datetime(2022, 10, 14, 22, 11, 39, 203487)}, [Amenity] (e1e8193f-0fff-40f1-91a7-8cf13c0564fc
) {'id': 'e1e8193f-0fff-40f1-91a7-8cf13c0564fc', 'created_at': datetime.datetime(2022, 10, 14
, 22, 12, 2, 152953), 'updated_at': datetime.datetime(2022, 10, 14, 22, 12, 2, 153014)}, [Cit
y] (c5b5305f-d366-4c44-9dca-9811201eaa9b) {'name': 'Tokyo', 'created_at': datetime.datetime(2
022, 10, 14, 22, 12, 44, 868360), 'updated_at': datetime.datetime(2022, 10, 14, 22, 12, 44, 8
68484), 'id': 'c5b5305f-d366-4c44-9dca-9811201eaa9b'}, [City] (3a8a6acd-e9c2-493b-b86d-5cbd64
596829) {'name': 'Rio', 'id': '3a8a6acd-e9c2-493b-b86d-5cbd64596829', 'created_at': datetime.
datetime(2022, 10, 14, 22, 13, 40, 848842), 'updated_at': datetime.datetime(2022, 10, 14, 22,
13, 40, 848903)}]
(hbnb)
```
  
**count**
- Usage: `count <class>` or `<class>.count()>`  

Retrieves the number of instances of a given class.
```
(hbnb) create Place
8362307e-c670-431c-b0a2-fd7b752c9ce8
(hbnb) create Place
8176bbbe-7e77-4391-84ba-688dbbb54b2c
(hbnb) create Place
69870576-f669-4baf-9639-877ee7432a42
(hbnb) create Place
fc4b9c16-00b4-4800-9cd1-26709c70c305
(hbnb) create User
20799a6f-7c58-4845-9074-ee8551c1c5fa
(hbnb) 
(hbnb) count Place
4
(hbnb) User.count()
1
(hbnb)
```
  
**update**
- Usage: `update <class> <id> <attribute name> "<attribute value>"`  

 Updates a class instance based on a given id with a given key/value attribute pair or dictionary of attribute pairs. If `update` is called with a single key/value attribute pair, only "simple" attributes can be updated (ie. not `id`, `created_at`, and `updated_at`).
```
(hbnb) create User
5ba3a902-e3ec-4ac8-9bbc-6b0866a34944
(hbnb) 
(hbnb) update User 5ba3a902-e3ec-4ac8-9bbc-6b0866a34944 first_name "Ubuntu"
(hbnb) show User 5ba3a902-e3ec-4ac8-9bbc-6b0866a34944
[User] (5ba3a902-e3ec-4ac8-9bbc-6b0866a34944) {'id': '5ba3a902-e3ec-4ac8-9bbc-6b0866a34944', 
'created_at': datetime.datetime(2022, 10, 14, 22, 23, 52, 716015), 'updated_at': datetime.da
tetime(2022, 10, 14, 22, 24, 52, 698398), 'first_name': 'Ubuntu'}
(hbnb) 
(hbnb) User.update(5ba3a902-e3ec-4ac8-9bbc-6b0866a34944, last_name="Snow")
(hbnb) show User 5ba3a902-e3ec-4ac8-9bbc-6b0866a34944
[User] (5ba3a902-e3ec-4ac8-9bbc-6b0866a34944) {'id': '5ba3a902-e3ec-4ac8-9bbc-6b0866a34944', 
 'created_at': datetime.datetime(2022, 10, 14, 22, 23, 52, 716015), 'updated_at': datetime.d
atetime(2022, 10, 14, 22, 26, 1, 969385), 'first_name': 'Ubuntu', 'last_name': 'Snow'}
(hbnb)
```

## Author :black_nib:
- **Chigozirim Igweamaka** - <[iChigozirim](https://github.com/iChigozirim)>
