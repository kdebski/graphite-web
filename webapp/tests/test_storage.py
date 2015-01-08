from graphite.remote_storage import RemoteStore
from django.test import TestCase


class StorageTest(TestCase):
  def test_remotestore_with_no_rules(self):
    remoteStore = RemoteStore('1.1.1.1')
    self.assertTrue(remoteStore.isMatchingRules('stats.test'))
    self.assertTrue(remoteStore.isAvailableForQuery('stats.test'))

  def test_remotestore_with_empty_rules(self):
    remoteStore = RemoteStore('1.1.1.1', [])
    self.assertTrue(remoteStore.isMatchingRules('stats.test'))
    self.assertTrue(remoteStore.isAvailableForQuery('stats.test'))

  def test_remotestore_with_valid_rules(self):
      remoteStore = RemoteStore('1.1.1.1', [{pattern:'^stats\\.', 'servers':['1.1.1.1']},
                                            {pattern:'^stats2\\.', 'servers':['2.2.2.2', '1.1.1.1']},
                                            {pattern:'^stats3\\.', 'servers':['2.2.2.2']}])
      self.assertTrue(remoteStore.isMatchingRules('stats.test'))
      self.assertTrue(remoteStore.isAvailableForQuery('stats.test'))

  def test_remotestore_with_invalid_rules(self):
    remoteStore = RemoteStore('1.1.1.1', [{pattern:'^stats2\\.', 'servers':['1.1.1.1']},
                                          {pattern:'^stats\\.', 'servers':['2.2.2.2']}])
    self.assertFalse(remoteStore.isMatchingRules('stats.test'))
    self.assertFalse(remoteStore.isAvailableForQuery('stats.test'))

  def test_remotestore_with_no_rules_for_host(self):
    remoteStore = RemoteStore('1.1.1.1', [{pattern:'^stats\\.', 'servers':['3.3.3.3']},
                                          {pattern:'^stats2\\.', 'servers':['2.2.2.2']}])
    self.assertFalse(remoteStore.isMatchingRules('stats.test'))
    self.assertFalse(remoteStore.isAvailableForQuery('stats.test'))

  def test_remotestore_with_None_rules(self):
      remoteStore = RemoteStore('1.1.1.1', None)
      self.assertTrue(remoteStore.isMatchingRules('stats.test'))
      self.assertTrue(remoteStore.isAvailableForQuery('stats.test'))
