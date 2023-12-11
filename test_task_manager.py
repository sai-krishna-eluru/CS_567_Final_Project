import unittest
import os
from io import StringIO
from unittest.mock import patch
from task_manager import Task, TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()
        self.task1 = Task("Complete project", 2)
        self.task2 = Task("Read a book", 1)
        self.task3 = Task("Go to the gym", 2)
        self.manager.add_task(self.task1)
        self.manager.add_task(self.task2)
        self.manager.add_task(self.task3)

    def test_add_task(self):
        new_task = Task("Write code", 3)
        self.manager.add_task(new_task)
        self.assertIn(new_task, self.manager.tasks)

    def test_get_priority_tasks(self):
        priority_2_tasks = self.manager.get_priority_tasks(2)
        self.assertEqual(priority_2_tasks, [self.task1, self.task3])

    def test_get_completed_tasks(self):
        self.manager.mark_task_as_completed(0)
        completed_tasks = self.manager.get_completed_tasks()
        self.assertEqual(completed_tasks, [self.task1])

    def test_mark_task_as_completed_valid_index(self):
        self.manager.mark_task_as_completed(1)
        self.assertTrue(self.task2.completed)

    def test_mark_task_as_completed_invalid_index(self):
        with self.assertRaises(ValueError):
            self.manager.mark_task_as_completed(5)

    def test_search_tasks(self):
        matching_tasks = self.manager.search_tasks("book")
        self.assertEqual(matching_tasks, [self.task2])

    def test_display_tasks(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.manager.display_tasks()
            expected_output = "1. Priority: 2, Description: Complete project, Status: Pending\n" \
                              "2. Priority: 1, Description: Read a book, Status: Pending\n" \
                              "3. Priority: 2, Description: Go to the gym, Status: Pending\n"
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_save_and_load_tasks(self):
        filename = "test_tasks.pkl"
        self.manager.save_tasks(filename)
        
        # Create a new manager instance and load tasks
        new_manager = TaskManager()
        new_manager.load_tasks(filename)

        # Print tasks for debugging
        print("Original tasks:", self.manager.tasks)
        print("Loaded tasks:", new_manager.tasks)

        # Check if loaded tasks are the same as the original ones
        self.assertEqual(len(new_manager.tasks), len(self.manager.tasks))
        self.assertTrue(all(task in new_manager.tasks for task in self.manager.tasks))

        # Clean up: remove the test file
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
