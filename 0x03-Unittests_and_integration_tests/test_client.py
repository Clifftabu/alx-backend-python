#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
Includes both unit and integration tests using mocks and parameterization.
"""

import unittest
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
import client


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class from client module"""

    @parameterized.expand([
        ('google_org', 'google', {'login': 'google', 'repo_url': 'https://api.github.com/orgs/google/repos'}),
        ('abc_org', 'abc', {'login': 'abc', 'repo_url': 'https://api.github.com/orgs/abc/repos'})
    ])
    @patch('client.get_json')
    def test_org(self, name, organization_name, expected_data, mock_get_json):
        """Test the .org method returns correct organization data."""
        mock_get_json.return_value = expected_data
        org_client = GithubOrgClient(organization_name)
        self.assertEqual(
            org_client.org,
            expected_data,
            f"The organization {organization_name} should provide expected results {expected_data}"
        )
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{organization_name}'
        )

    def test_public_repos_url(self):
        """Test the _public_repos_url property returns the correct URL."""
        payload = {"repos_url": "https://example.com/example_org/repos"}
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client_instance = GithubOrgClient('example_org')
            self.assertEqual(
                client_instance._public_repos_url,
                "https://example.com/example_org/repos",
                "Should return repository URL"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected repo names."""
        test_repos = [
            {'name': 'repo_1', 'license': "license_for_repo_1"},
            {'name': 'repo_2', 'license': 'license for repo_2'}
        ]
        mock_get_json.return_value = test_repos
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = 'https://api.github.com/example_org/repos'
            client_instance = GithubOrgClient('example_org')
            self.assertEqual(
                client_instance.public_repos(),
                ['repo_1', 'repo_2'],
                'Should return a list of repository names'
            )
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/example_org/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean based on repo license key."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected,
            'Should return a license key'
        )


@parameterized_class([{
    'org_payload': {'repos_url': "https://api.github.com/example_org/repos"},
    'repos_payload': [{'name': 'repo_1'}, {'name': 'repo_2'}],
    'expected_repos': ['repo_1', 'repo_2']
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient using mock requests."""

    @classmethod
    def setUpClass(cls):
        """Set up mocks before all tests."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            Mock(json=Mock(return_value=cls.org_payload)),  # First call
            Mock(json=Mock(return_value=cls.repos_payload))  # Second call
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop mock patching after all tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos method."""
        client_instance = GithubOrgClient('test')
        result = client_instance.public_repos()
        self.assertEqual(result, self.expected_repos)
