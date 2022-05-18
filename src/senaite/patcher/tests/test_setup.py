# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from senaite.patcher.testing import SENAITE_PATCHER_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that senaite.patcher is properly installed."""

    layer = SENAITE_PATCHER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if senaite.patcher is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'senaite.patcher'))

    def test_browserlayer(self):
        """Test that ISenaitePatcherLayer is registered."""
        from senaite.patcher.interfaces import (
            ISenaitePatcherLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ISenaitePatcherLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = SENAITE_PATCHER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['senaite.patcher'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if senaite.patcher is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'senaite.patcher'))

    def test_browserlayer_removed(self):
        """Test that ISenaitePatcherLayer is removed."""
        from senaite.patcher.interfaces import \
            ISenaitePatcherLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ISenaitePatcherLayer,
            utils.registered_layers())
