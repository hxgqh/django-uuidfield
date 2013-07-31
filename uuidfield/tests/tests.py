import uuid

from django.db import connection, IntegrityError
from django.test import TestCase

from uuidfield.tests.models import (AutoUUIDField, ManualUUIDField,
    NamespaceUUIDField, BrokenNamespaceUUIDField, HyphenatedUUIDField)


class UUIDFieldTestCase(TestCase):

    def test_auto_uuid4(self):
        obj = AutoUUIDField.objects.create()
        self.assertTrue(obj.uuid)
        self.assertEquals(len(obj.uuid), 32)
        self.assertTrue(isinstance(obj.uuid, uuid.UUID))
        self.assertEquals(obj.uuid.version, 4)

    def test_raises_exception(self):
        self.assertRaises(IntegrityError, ManualUUIDField.objects.create)

    def test_manual(self):
        obj = ManualUUIDField.objects.create(uuid=uuid.uuid4())
        self.assertTrue(obj)
        self.assertEquals(len(obj.uuid), 32)
        self.assertTrue(isinstance(obj.uuid, uuid.UUID))
        self.assertEquals(obj.uuid.version, 4)

    def test_namespace(self):
        obj = NamespaceUUIDField.objects.create()
        self.assertTrue(obj)
        self.assertEquals(len(obj.uuid), 32)
        self.assertTrue(isinstance(obj.uuid, uuid.UUID))
        self.assertEquals(obj.uuid.version, 5)

    def test_broken_namespace(self):
        self.assertRaises(ValueError, BrokenNamespaceUUIDField.objects.create)

    def test_hyphenated(self):
        obj = HyphenatedUUIDField.objects.create(name='test')
        uuid = obj.uuid

        self.assertTrue('-' in unicode(uuid))
        self.assertTrue('-' in str(uuid))

        self.assertEquals(len(uuid), 36)

        # ensure the hyphens don't affect re-saving object
        obj.name = 'shoe'
        obj.save()

        obj = HyphenatedUUIDField.objects.get(uuid=obj.uuid)

        self.assertTrue(obj.uuid, uuid)
        self.assertTrue(obj.name, 'shoe')
