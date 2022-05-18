# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import senaite.patcher


class SenaitePatcherLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=senaite.patcher)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'senaite.patcher:default')


SENAITE_PATCHER_FIXTURE = SenaitePatcherLayer()


SENAITE_PATCHER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SENAITE_PATCHER_FIXTURE,),
    name='SenaitePatcherLayer:IntegrationTesting',
)


SENAITE_PATCHER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SENAITE_PATCHER_FIXTURE,),
    name='SenaitePatcherLayer:FunctionalTesting',
)


SENAITE_PATCHER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        SENAITE_PATCHER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='SenaitePatcherLayer:AcceptanceTesting',
)
