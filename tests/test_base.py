import unittest

from goo import create_all, drop_all
from .test_object import TestObject


class TestBase(unittest.TestCase):
    def setUp(self):
        create_all()

    def tearDown(self):
        drop_all()

    def test_create(self):
        obj = TestObject.create(name='John', counter=1)
        self.assertIsNotNone(obj, "fail to create object")
        obj.commit()

        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.name, 'John')
        self.assertIsNotNone(obj.created_at)
        self.assertEqual(obj.counter, 1)

        return obj

    def validate_objects(self, obj1, obj2):
        self.assertIsNotNone(obj1)
        self.assertIsNotNone(obj2)

        self.assertIsNotNone(obj1.id)
        self.assertIsNotNone(obj2.id)
        self.assertEqual(obj1.id, obj2.id)

        self.assertIsNotNone(obj1.name)
        self.assertIsNotNone(obj2.name)
        self.assertEqual(obj1.name, obj2.name)

        self.assertIsNotNone(obj1.created_at)
        self.assertIsNotNone(obj2.created_at)
        self.assertEqual(obj1.created_at, obj2.created_at)

        self.assertIsNotNone(obj1.counter)
        self.assertIsNotNone(obj2.counter)
        self.assertEqual(obj1.counter, obj2.counter)

    def test_get_id(self):
        new_obj = self.test_create()

        obj = TestObject.get(id=new_obj.id)
        self.assertIsNotNone(obj, "fail to retrieve object with name 'John'")

        self.validate_objects(new_obj, obj)

    def test_get_name(self):
        new_obj = self.test_create()

        obj = TestObject.get(filter_by={'name': new_obj.name})
        self.assertIsNotNone(obj, "fail to retrieve object with name 'John'")

        self.validate_objects(new_obj, obj)

    def test_get_unknown(self):
        obj = TestObject.get(filter_by={'name': 'Edouardo'})
        self.assertIsNone(obj, "got an obj for name 'Eduardo', should not")

    def test_list(self):
        new_obj = self.test_create()

        obj_list = TestObject.list()
        self.assertIsNotNone(obj_list, "fail to retrieve object list")
        self.assertEqual(len(obj_list), 1)
        self.validate_objects(new_obj, obj_list[0])

    def test_list_empty(self):
        obj_list = TestObject.list()
        self.assertTrue(not obj_list)

    def test_update(self):
        obj = self.test_create()

        obj.update(counter=42).commit()
        self.assertEqual(obj.counter, 42)

        obj2 = TestObject.get(id=obj.id)
        self.assertIsNotNone(obj2)

        self.validate_objects(obj, obj2)

    def test_delete(self):
        obj = self.test_create()

        obj_id = obj.id
        obj_dict = obj.delete()
        self.assertIsNotNone(obj_dict)
        self.assertEqual(obj_dict['id'], obj_id)

        obj = TestObject.get(id=obj_id)
        self.assertIsNone(obj)



if __name__ == '__main__':
    unittest.main()
