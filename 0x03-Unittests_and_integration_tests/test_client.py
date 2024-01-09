#!/usr/bin/env python3
"""
Unittests for client.py
"""
import unittest
from parameterized import parameterized
from typing import Union, Dict, Tuple
from unittest.mock import Mock, patch, MagicMock, PropertyMock

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test the GithubOrgClient's function
    """
    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch(
        "client.get_json",
    )
    def test_org(self, org: str, resp: Dict, mocked_fxn: MagicMock) -> None:
        """
        Test GithubOrgClient's expected output
        """
        mocked_fxn.return_value = MagicMock(return_value=resp)
        gh_org_client = GithubOrgClient(org)
        self.assertEqual(gh_org_client.org(), resp)
        mocked_fxn.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )

    def test_public_repos_url(self) -> None:
        """
        Test for _public_repos_url's expected output
        """
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
                ) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos",
                )
