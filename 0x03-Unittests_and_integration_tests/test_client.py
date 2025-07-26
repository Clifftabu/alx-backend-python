#!/usr/bin/env python3
"""
Unit and integration tests for GithubOrgClient
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch('client.get_json')
    def test_org(self, name, organization_name, expected_data, mock_get_json):
        """Test that GithubOrgClient.org returns correct data."""
        mock_get_json.return_value = expected_data
        client = GithubOrgClient(organization_name)
        self.assertEqual(client.org, expected_data)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{organization_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org payload."""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/users/google/repos"}
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "https://api.github.com/users/google/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of repo names."""
        payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = payload
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license correctly checks for repo license key."""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using mocked HTTP responses."""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get with example payloads before all tests."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        mock_get.side_effect = [
            unittest.mock.Mock(**{'json.return_value': cls.org_payload}),
            unittest.mock.Mock(**{'json.return_value': cls.repos_payload}),
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get after all tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo list."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters by Apache-2.0 license."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
