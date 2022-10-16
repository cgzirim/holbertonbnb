#!/usr/bin/python3
"""
Defines unittests for console.py
"""
import os
import models
import console
import unittest
from io import StringIO
from unittest.mock import patch
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

HBNBCommand = console.HBNBCommand


class TestHBNBCommandWithFileStorage(unittest.TestCase):
    """Unittests for testing the HBNB console with FileStorage"""

    @classmethod
    def setUpClass(cls):
        """Testing setup.

        Rename any existing file.json temporarily.
        Create an instance of the command interpreter.
        """
        try:
            os.rename("file.json", "original")
        except IOError:
            pass
        cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Testing teardown.

        Restore original file.json.
        Delete the test HBNBCommand instance.
        """
        try:
            os.rename("original", "file.json")
        except IOError:
            pass
        del cls.HBNB
        if type(models.storage) == DBStorage:
            models.storage._DBStorage__session.close()

    def setUp(self):
        """Reset FileStorage objects dictionary."""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Delete any created file.json."""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_docstrings(self):
        """Check all methods have docstrings."""
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.preloop.__doc__)
        self.assertIsNotNone(HBNBCommand.postloop.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)

        self.assertIsNotNone(HBNBCommand.help_Amenity.__doc__)
        self.assertIsNotNone(HBNBCommand.help_BaseModel.__doc__)
        self.assertIsNotNone(HBNBCommand.help_City.__doc__)
        self.assertIsNotNone(HBNBCommand.help_Place.__doc__)
        self.assertIsNotNone(HBNBCommand.help_Review.__doc__)
        self.assertIsNotNone(HBNBCommand.help_State.__doc__)

        self.assertIsNotNone(HBNBCommand.complete_all.__doc__)
        self.assertIsNotNone(HBNBCommand.complete_count.__doc__)
        self.assertIsNotNone(HBNBCommand.complete_create.__doc__)
        self.assertIsNotNone(HBNBCommand.complete_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.complete_show.__doc__)
        self.assertIsNotNone(HBNBCommand.complete_update.__doc__)

    @patch("sys.stdout", new_callable=StringIO)
    def test_emptyline(self, mock_stdout):
        """Test empty line input."""
        self.HBNB.onecmd("\n")
        self.assertEqual("", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_quit(self, mock_stdout):
        """Test the quit command."""
        self.HBNB.onecmd("quit")
        self.assertEqual("", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_quit(self, mock_stdout):
        """Test the quit command."""
        self.HBNB.onecmd("quit")
        self.assertEqual("", mock_stdout.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    @patch("sys.stdout", new_callable=StringIO)
    def test_create(self, mock_stdout):
        """Test the create command on all models."""
        models = [
            "BaseModel", "Amenity", "City", "State", "Place", "User", "Review"]

        models_uuids = []
        for model in models:
            self.HBNB.onecmd(f"create {model}")
            models_uuids.append(mock_stdout.getvalue())

        for uuid in models_uuids:
            self.HBNB.onecmd(f"all {model}")
            self.assertIn(uuid, mock_stdout.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create_kwargs(self):
        """Test the create command with kwargs."""
        with patch("sys.stdout", new=StringIO()) as f:
            kwargs = (
                'create Place city_id="1234" name="Johnsons" '
                "number_rooms=3 latitude=24.89 longitude=f"
            )
            self.HBNB.onecmd(kwargs)
            placeId = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            output = f.getvalue()
            self.assertIn(placeId, output)
            self.assertIn("'city_id': '1234'", output)
            self.assertIn("'name': 'Johnsons'", output)
            self.assertIn("'number_rooms': 3", output)
            self.assertIn("'latitude': 24.89", output)
            self.assertNotIn("'longitude'", output)

    def test_create_error_messages(self):
        """Test create command error messages."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create asdfsfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_count(self):
        """Test the count command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("count abcd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("count Place")
            self.assertEqual("0\n", f.getvalue())

    def test_show(self):
        """Test the show command."""
        call = [
            ["show", "** class name missing **\n"],
            ["show abc", "** class doesn't exist **\n"],
            ["show BaseModel", "** instance id missing **\n"],
            ["show BaseModel abc-123", "** no instance found **\n"],
        ]
        for input, expected_output in call:
            with patch("sys.stdout", new=StringIO()) as f:
                self.HBNB.onecmd(input)
                self.assertEqual(expected_output, f.getvalue())

    def test_destroy(self):
        """Test the destroy command."""
        call = [
            ["destroy", "** class name missing **\n"],
            ["destroy abc", "** class doesn't exist **\n"],
            ["destroy BaseModel", "** instance id missing **\n"],
            ["destroy BaseModel abc-123", "** no instance found **\n"],
        ]
        for input, expected_output in call:
            with patch("sys.stdout", new=StringIO()) as f:
                self.HBNB.onecmd(input)
                self.assertEqual(expected_output, f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_all(self):
        """Test the all command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all abc")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            self.assertEqual("[]\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_update(self):
        """Test the update command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create User")
            usr_id = f.getvalue()

        call = [
            ["update", "** class name missing **\n"],
            ["update abc", "** class doesn't exist **\n"],
            ["update User", "** instance id missing **\n"],
            ["update User abc-123", "** no instance found **\n"],
            [f"update User {usr_id}", "** attribute name missing **\n"],
            [f"update User {usr_id} Name", "** value missing **\n"],
        ]
        for input, expected_output in call:
            with patch("sys.stdout", new=StringIO()) as f:
                self.HBNB.onecmd(input)
                self.assertEqual(expected_output, f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    @patch("sys.stdout", new_callable=StringIO)
    def test_create(self, mock_stdout):
        """Test the alternate create command on all models."""
        models = [
            "BaseModel", "Amenity", "City", "State", "Place", "User", "Review"]

        models_uuids = []
        for model in models:
            self.HBNB.onecmd(f"{model}.create()")
            models_uuids.append(mock_stdout.getvalue())

        for uuid in models_uuids:
            self.HBNB.onecmd(f"all {model}")
            self.assertIn(uuid, mock_stdout.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_alt_count(self):
        """Test the alternate count command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("asdfsdfsd.count()")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("State.count()")
            self.assertEqual("0\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_alt_all(self):
        """Test alternate all command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("abc.all()")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("Place.all()")
            self.assertEqual("[]\n", f.getvalue())

    def test_alt_show(self):
        """Test the alternate show command."""
        call = [
            ["abc.show()", "** class doesn't exist **\n"],
            ["BaseModel.show()", "** instance id missing **\n"],
            ["BaseModel.show(abc-123)", "** no instance found **\n"],
        ]
        for input, expected_output in call:
            with patch("sys.stdout", new=StringIO()) as f:
                self.HBNB.onecmd(input)
                self.assertEqual(expected_output, f.getvalue())

    def test_alt_destroy(self):
        """Test the alternate destroy command."""
        call = [
            ["abc.destroy()", "** class doesn't exist **\n"],
            ["BaseModel.destroy()", "** instance id missing **\n"],
            ["BaseModel.destroy(abc-123)", "** no instance found **\n"],
        ]
        for input, expected_output in call:
            with patch("sys.stdout", new=StringIO()) as f:
                self.HBNB.onecmd(input)
                self.assertEqual(expected_output, f.getvalue())

    def test_alt_update(self):
        """Test the alternate update command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create User")
            usr_id = f.getvalue()

        call = [
            ["abc.update()", "** class doesn't exist **\n"],
            ["User.update()", "** instance id missing **\n"],
            ["User.update(abc-123)", "** no instance found **\n"],
            [f"User.update({usr_id})", "** attribute name missing **\n"],
            [f"User.update({usr_id}, name)", "** value missing **\n"],
        ]
        for input, expected_output in call:
            with patch("sys.stdout", new=StringIO()) as f:
                self.HBNB.onecmd(input)
                self.assertEqual(expected_output, f.getvalue())


if __name__ == "__main__":
    unittest.main()
