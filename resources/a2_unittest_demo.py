
"""
Unit test example.

This is the code for the unittest example we ran in class. I have left the tests in place for
you to use as a reference, but remember, they will not run on your a2. You must replace the a2.*
function calls with the code that you wrote in your a2 or input_processor modules.

by Mark S Baldwin
"""

import a2 as a2
import unittest
from pathlib import Path

class CommandTestBase(unittest.TestCase):
    def assertIsDsuFile(self, path):
        if not Path(path).resolve().is_file():
            raise AssertionError(f"DSU file does not exist: {path}")

class CommandTest(CommandTestBase):
    dsu_path = "/home/mark/ics32" #replace with path on local system
    dsu_name = "myprofile"
    # replace with your info
    usr = "markb"
    pwd = "pwd123"
    bio = "My bio test"
    msg = "First Post!"

    def test_C_cmd(self):
        a2.handle_input(f"C {self.dsu_path} -n {self.dsu_name}")
        self.assertIsDsuFile(f"{self.dsu_path}/{self.dsu_name}.dsu")
    
    def test_O_cmd(self):
        a2.handle_input(f"O {self.dsu_path}/{self.dsu_name}.dsu")
        self.assertIsNotNone(a2._cur_profile_path)
    
    def test_E_cmd(self):
        a2.handle_input(f"O {self.dsu_path}/{self.dsu_name}.dsu")
        a2.handle_input(f"E -usr \"{self.usr}\" -pwd \"{self.pwd}\" -bio \"{self.bio}\"")
        self.assertEqual(a2._cur_profile.username, self.usr)
        self.assertEqual(a2._cur_profile.password, self.pwd)
        self.assertEqual(a2._cur_profile.bio, self.bio)

    def test_E_addpost_cmd(self):
        a2.handle_input(f"O {self.dsu_path}/{self.dsu_name}.dsu")
        a2.handle_input(f"E -addpost \"{self.msg}\"")
        posts = a2._cur_profile.get_posts()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].get_entry(), self.msg)
    
    def test_E_delpost_cmd(self):
        a2.handle_input(f"O {self.dsu_path}/{self.dsu_name}.dsu")
        a2.handle_input("E -delpost 0")
        posts = a2._cur_profile.get_posts()
        self.assertEqual(len(posts), 0)

    
if __name__ == '__main__':
    #delete test file before running tests
    myprofile = Path(f"{CommandTest.dsu_path}/{CommandTest.dsu_name}.dsu")
    myprofile.unlink(missing_ok=True)
    
    unittest.main()
