##Project Structure
utils.py: Contains utility functions for nested map access, JSON fetching, and memoization.
test_utils.py: Unit tests for utility functions, including parameterized tests and mocking.
client.py: A sample GitHub organization client.
test_client.py: Unit and integration tests for the GitHub client, including property mocking and fixture-based tests.
fixtures.py: Example data used for integration tests.

Task 1: Parameterize a Unit Test for Exceptions
Implemented TestAccessNestedMap.test_access_nested_map_exception using @parameterized.expand.

Tested that access_nested_map raises a KeyError for invalid paths:

nested_map={}, path=("a",)

nested_map={"a": 1}, path=("a", "b")

Used assertRaises to check for the exception and verified that the exception message matches the missing key.

Ensured robust error handling and improved test coverage for edge cases.

