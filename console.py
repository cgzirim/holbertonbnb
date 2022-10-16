#!/usr/bin/python3
""" Module for the console """

import cmd
import sys
import models
import signal
from os import getenv
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex  # for splitting the line along spaces except in double quotes

classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}

if getenv("HBNB_TYPE_STORAGE") == "db":
    del classes["BaseModel"]


class HBNBCommand(cmd.Cmd):
    """HBNH console"""

    prompt = "(hbnb) "

    def preloop(self):
        """Handles intro to command interpreter."""
        print(".----------------------------.")
        print("|    Welcome to hbnb CLI!    |")
        print("|   for help, input 'help'   |")
        print("|   for quit, input 'quit'   |")
        print(".----------------------------.")

    def postloop(self):
        """Handles exit to command interpreter."""
        print(".----------------------------.")
        print("|  Well, that sure was fun!  |")
        print(".----------------------------.")

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """overwriting the emptyline method"""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def default(self, arg):
        """Default behavior for cmd module."""
        cmds = {
            "all": self.do_all,
            "count": self.do_count,
            "create": self.do_create,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
        }
        if "." in arg and "(" in arg and ")" in arg:
            cls = arg[:arg.index(".")]
            method = arg[arg.index(".") + 1:arg.index("(")]
            arguments = arg[arg.index("(") + 1:arg.index(")")]
            arguments = arguments.replace("=", " ")
            arguments = "{} {}".format(cls, arguments.replace(",", ""))
            if method in cmds.keys():
                return cmds[method](arguments)
        self.stdout.write("*** Unknown syntax: %s\n" % arg)
        return

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split("=", 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace("_", " ")
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Creates a new instance of a class.
        Usage: create <class> <param 1> <param 2> ..., or
               <class>.create(<param 1> <param 2> ...)
        Ex: (hbnb) create City name="Tokyo"
            (hbnb) City.create(name="Tokyo")
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Prints the string representation of an instance based on its class
        and ID.

        Usage: show <class> <id> or <class>.show(<id>)
        Ex: (hbnb) show City 1234-abcd-5678-efgh
            (hbnb) City.show(1234-abcd-5678-efgh)
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on its class and ID.
        Usage: destroy <class> <id> or <class>.destroy(<id>)
        Ex: (hbnb) destroy City 1234-abcd-5678-efgh
            (hbnb) City.destroy(1234-abcd-5678-efgh)
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    if getenv("HBNB_TYPE_STORAGE") == "db":
                        instance = models.storage.all()[key]
                        instance.delete()
                    else:
                        models.storage.all().pop(key)
                        models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Displays string representation of all instances of a given class.
        If no class is specified, displays all instantiated objects.

        Usage: all or all <class> or <class>.all()
        Ex: (hbnb) all
            (hbnb) all BaseModel
            (hbnb) BaseModel.all()
        """
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_count(self, arg):
        """Retrieves the number of instances of a class.
        Usage: count <class> or <class>.count()
        Ex: (hbnb) count City
            (hbnb) City.count()
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in classes:
            print("** class doesn't exist **")
            return False

        count = 0
        for key in models.storage.all().keys():
            if args[0] in key:
                count += 1
        print(count)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding
        or updating an attribute.

        Usage: update <class name> <id> <attribute name> <attribute value> or
                <class name>.update(<id>, <attribute name>, <attribute value>)
        Ex: (hbnb) update City 1234-abcd-5678-efgh name Chicago
            (hbnb) City.update(1234-abcd-5678-efgh, name, Chicago)
            (hbnb) City.update(1234-abcd, {'name': 'Chicago', 'address': 'None'})
        """
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest", "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    # Define methods to display help for each class:

    def help_BaseModel(self):
        """Help for the BaseModel class."""
        message = """A class which other classes inherit from.
            Usage: <command> BaseModel or BaseModel.<command>()
        """
        print(message)

    def help_Amenity(self):
        """Help for Amenity class."""
        message = """A class which represents an amenity.
        Usage: <command> Amenity or Amenity.<command>()

        Required attributes (columns) to create an Amenity:
            attr_name |  data-type |  mandatory
            -----------------------------------
            name      |  string    |  yes
            
        Ex: (hbnb) create Amenity name="Wifi" or
            (hbnb) Amenity.create(name="Wifi")
        """

        print(message)

    def help_City(self):
        """Help for City class."""
        message = """A class which represents a city.
        Usage: <command> City or City.<command>()

        Required attributes (columns) to create a City:
            attr_name |  data-type |  mandatory
            -----------------------------------
            name      |  string    |  yes
            state_id  |  string    |  yes
        
        Ex: (hbnb) create City name="Tokyo" state_id="1234-abcd-efgh-54678" or
            (hbnb) City.create(name="Tokyo" state_id="1234-abcd-efgh-54678")
        """

        print(message)

    def help_Place(self):
        """Help for Place class."""
        message = """A class which represents a place.
        Usage: <command> Place or Place.<command>()
        
        Required attributes (columns) to create a Place:
            attr_name       |  data-type |  mandatory
            -----------------------------------------
            name            |  string    |  yes
            city_id         |  string    |  yes
            state_id        |  string    |  yes
            number_rooms    |  integer   |  yes
            number_bathrooms|  integer   |  yes
            max_guest       |  integer   |  yes
            price_by_night  |  integer   |  yes
            description     |  string    |  no
            latitude        |  float     |  no
            longitude       |  float     |  no
            amenity_ids     |  list      |  no

        Ex: (hbnb) create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297
        or  (hbnb) Place.create(create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297)
        """
        print(message)

    def help_Review(self):
        """Help for Review class."""
        message = """A class which represents a review.
        Usage: <command> Review or Review.<command>()
        
        Required attributes (columns) to create a Review:
            attr_name |  data-type |  mandatory
            -----------------------------------
            place_id  |  string    |  yes
            user_id   |  string    |  yes
            text      |  string    |  yes

        Ex: (hbnb) create Review place_id="123-abc-456-def" user_id="123-abc-456-def" text="Amazing_place,_huge_kitchen"
        or  (hbnb) Review.create(place_id="123-abc-456-def" user_id="123-abc-456-def" text="Amazing_place,_huge_kitchen")
        """
        print(message)

    def help_State(self):
        """Help for State class."""
        message = """A class which represents a state.
        Usage: <command> State or State.<command>()
        
        Required attributes (columns) to create a State:
            attr_name |  data-type |  mandatory
            -----------------------------------
            name      |  string    |  yes

        Ex: (hbnb) Create State name="California" or
            (hbnb) State.create(name="California")
        """
        print(message)

    def help_User(self):
        """Help for User class."""
        message = """A class which represents a user.
        Usage: <command> User or User.<command>()

        Required attributes (columns) to create a User:
            attr_name  |  data-type |  mandatory
            ------------------------------------
            first_name |  string    |  yes
            last_name  |  string    |  yes
            email      |  string    |  yes
            password   |  string    |  yes

        Ex: (hbnb) create User email="gui@example.com" password="guipwd" first_name="Guillaume" last_name="Snow"
        or  (hbnb) User.create(email="gui@example.com" password="guipwd" first_name="Guillaume" last_name="Snow")
        """
        print(message)

    # Implement autocomplete for commands:

    def complete_all(self, text, line, begidx, endidx):
        """Auto complete for create command"""
        if not text:
            completions = [cls for cls in classes.keys()]
        else:
            text = text.capitalize()
            completions = [cls for cls in classes.keys() if cls.startswith(text)]

        return completions

    def complete_count(self, text, line, begidx, endidx):
        """Auto complete for create command"""
        if not text:
            completions = [cls for cls in classes.keys()]
        else:
            text = text.capitalize()
            completions = [cls for cls in classes.keys() if cls.startswith(text)]

        return completions

    def complete_create(self, text, line, begidx, endidx):
        """Auto complete for create command"""
        if not text:
            completions = [cls for cls in classes.keys()]
        else:
            text = text.capitalize()
            completions = [cls for cls in classes.keys() if cls.startswith(text)]

        return completions

    def complete_destroy(self, text, line, begidx, endidx):
        """Auto complete for create command"""
        if not text:
            completions = [cls for cls in classes.keys()]
        else:
            text = text.capitalize()
            completions = [cls for cls in classes.keys() if cls.startswith(text)]

        return completions

    def complete_show(self, text, line, begidx, endidx):
        """Auto complete for create command"""
        if not text:
            completions = [cls for cls in classes.keys()]
        else:
            text = text.capitalize()
            completions = [cls for cls in classes.keys() if cls.startswith(text)]

        return completions

    def complete_update(self, text, line, begidx, endidx):
        """Auto complete for create command"""
        if not text:
            completions = [cls for cls in classes.keys()]
        else:
            text = text.capitalize()
            completions = [cls for cls in classes.keys() if cls.startswith(text)]

        return completions


def signal_handler(sig, frame):
    """Handle SIGNINT"""
    print("exiting...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    HBNBCommand().cmdloop()
