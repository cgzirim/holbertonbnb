#!/usr/bin/python3
""" console """

import cmd
from datetime import datetime
import models
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
        """Default behavior for cmd module when input is invalid."""
        cmds = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
        }
        if "." in arg and "(" in arg and ")" in arg:
            cls = arg[: arg.index(".")]
            method = arg[arg.index(".") + 1: arg.index("(")]
            argument = arg[arg.index("(") + 1: arg.index(")")]
            argument = "{} {}".format(cls, argument.replace(",", ""))
            if method in cmds.keys():
                return cmds[method](argument)
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

        Usage: create <class> or <class>.create()
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

    def do_classes(self, arg):
        """Lists all available classes with "classes" or detailed class
        with "classes class_name".
        """
        args = arg.split()
        if len(args) == 0:
            print("Available classes are:")
            for name, obj in classes.items():
                print("\t{}".format(name))
            print("""Use the command 'classes <class_name>' to learn how
                to create any of the classes above.""")
            return

        if args[0] not in classes:
            print("** class doesn't exist **")
            return False

        all_classes = {
            "Amenity": 'create Amenity name="Hot tube"',
            "City": 'create City state_id="95a5abab-aa65-4861-9bc6-1da4a36069aa" name="San_Francisco"',
            "Place": 'create Place city_id="4b457e66-c7c8-4f63-910f-fd91c3b7140b" user_id="4f3f4b42-a4c3-4c20-a492-efff10d00c0b" name="Lovely_place" number_rooms=3 number_bathrooms=1 max_guest=6 price_by_night=120 latitude=37.773972 longitude=-122.431297',
            "Review": 'create Review place_id="ed72aa02-3286-4891-acbc-9d9fc80a1103" user_id="d93638d9-8233-4124-8f4e-17786592908b" text="Amazing_place,_huge_kitchen"',
            "State": 'create State name="California"',
            "User": 'create User email="gui@hbtn.io" password="guipwd" first_name="Guillaume" last_name="Snow"',
        }

        usage = {
            "Amenity": "create Amenity <amenity_name>",
            "City": "create City <state_id> <city_name>",
            "Review": "create Review <place_id> <user_id> <text>",
            "State": "create State <name>",
            "User": "create User <email> <password> <first_name> <last_name>",
            "Place": "create Place <city_id> <user_id> <place_name> <number_rooms> <number_bathrooms> <max_guest> <price_by_night> <longitude> <latitude>"
        }

        print("Usage: {}\n".format(usage[args[0]]) )
        print("\nExample of use:")
        print("{}\n".format(all_classes[args[0]]))
        print("Class documentation:")
        print(classes[args[0]].__doc__)


    def do_show(self, arg):
        """Prints the string representation of an instance based on the class
        name and id.

        Usage: show <class> <id> or <class>.show()
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
        """Deletes an instance based on the class name and id.

        Usage: destroy <class> <id> or <class>.destroy(<id>)
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
        """Prints all string representation of all instances based or not on
        the class name.

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
        """Displays the number of instances of a class.

        Usage: count <class_name> or <class_name>.count()
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

        Usage: update <class name> <id> <attribute name> "<attribute value>" or
                <class name>.update(<id>, <attribute name>, <attribute value>)
        """
        args = shlex.split(arg)
        integers = [
            "number_rooms",
            "number_bathrooms",
            "max_guest",
            "price_by_night"
        ]
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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
