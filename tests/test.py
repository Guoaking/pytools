import asyncio
import unittest

from api import bit_playwright


class MyTestCase(unittest.TestCase):

    def test_FindElement(self):
        asyncio.run(bit_playwright.findEle("99ec4fd12fad403d8142b13be677d326"))

    def test_postconfig(self):
        print("111")
        return "111"


def test_something(self):
    self.assertEqual(True, False)  # add assertion here


if __name__ == "__main__":
    unittest.main()
