from django.test import TestCase
from rest_framework.test import APIClient
from sinp_nomenclatures.models import Nomenclature

from cables.models import Operation
from commons.tests.tests_commons import createTestUser, logTestUser
from media.models import Media


class OperationsAnonymousAuthenticationTestCase(TestCase):
    """Class to test authentication/permission scheme for Operation and anonymous user.

    Include tests for user trying to log-in with wrong password
    """

    # fixture includes:
    # - at least 2 points, 2 lines, 3 diagnosis, 3 operations, 2 GeoAreas, 2 SensitiveAreas, 2
    # (pictures), 2 mortality cases
    # - It contains needed sinp_nomenclature items (stand for dictionanry for specific data)
    fixtures = [
        "commons/tests/fixtures/test_nomenclatures.xml",
        "commons/tests/fixtures/test_cables.xml",
    ]

    def setUp(self):
        self.anonymous_client = APIClient()
        # create user trying to log-in with wrong password
        self.user = createTestUser("user", "password")
        self.unauthentified_client = logTestUser("user", "wrong-password")
        # get pk from the first Operation
        self.pk = Operation.objects.all()[0].id

    def test_get_list_with_anonymous_user(self):
        resp = self.anonymous_client.get("/api/v1/cables/operations/")
        self.assertEqual(resp.status_code, 401)
        resp = self.unauthentified_client.get("/api/v1/cables/operations/")
        self.assertEqual(resp.status_code, 401)

    def test_get_detail_with_anonymous_user(self):
        resp = self.anonymous_client.get(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 401)
        resp = self.unauthentified_client.get(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 401)

    def test_create_with_anonymous_user(self):
        resp = self.anonymous_client.post("/api/v1/cables/operations/")
        self.assertEqual(resp.status_code, 401)
        resp = self.unauthentified_client.post("/api/v1/cables/operations/")
        self.assertEqual(resp.status_code, 401)

    def test_update_with_anonymous_user(self):
        resp = self.anonymous_client.put(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 401)
        resp = self.unauthentified_client.put(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 401)

    def test_partial_update_with_anonymous_user(self):
        resp = self.anonymous_client.patch(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 401)
        resp = self.unauthentified_client.patch(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 401)

    def test_partial_delete_with_anonymous_user(self):
        resp = self.anonymous_client.delete(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 401)
        resp = self.unauthentified_client.delete(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 401)


class OperationUnauthorizedAuthenticationTestCase(TestCase):
    """Class to test authentication/permission scheme for Operation and unauthorized user."""

    # fixture includes:
    # - at least 2 points, 2 lines, 3 diagnosis, 3 operations, 2 GeoAreas, 2 SensitiveAreas, 2
    # (pictures), 2 mortality cases
    # - It contains needed sinp_nomenclature items (stand for dictionanry for specific data)
    fixtures = [
        "commons/tests/fixtures/test_nomenclatures.xml",
        "commons/tests/fixtures/test_cables.xml",
    ]

    def setUp(self):
        self.user = createTestUser("user", "password")
        self.unauthorized_client = logTestUser("user", "password")
        # get pk from the first Operation
        self.pk = Operation.objects.all()[0].id

    # no restriction for read only by default with Django
    def test_get_list_with_unauthorized_user(self):
        resp = self.unauthorized_client.get("/api/v1/cables/operations/")
        self.assertEqual(resp.status_code, 200)

    # no restriction for read only by default with Django
    def test_get_detail_with_unauthorized_user(self):
        resp = self.unauthorized_client.get(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 200)

    def test_create_with_unauthorized_user(self):
        resp = self.unauthorized_client.post(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 403)

    def test_update_with_unauthorized_user(self):
        resp = self.unauthorized_client.put(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 403)

    def test_partial_update_with_unauthorized_user(self):
        resp = self.unauthorized_client.patch(
            f"/api/v1/cables/operations/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 403)

    def test_partial_delete_with_unauthorized_user(self):
        resp = self.unauthorized_client.delete(
            f"/api/v1/cables/points/{self.pk}/"
        )
        self.assertEqual(resp.status_code, 403)


class CreatePointOperationTestCase(TestCase):
    """Class to test creation of Diagnosis related to Point infrastructure.
    This test case mainly focuses on automatic following specific function:
    When first Diagnosis is created from an infrastructure, it has last=True.
    When another one is created for this same infrastructure, the old one is set with last=False and the new one with last=True

    Require creation and consultation of various elements
    """

    # fixture includes:
    # - sinp_nomenclature items (stand for dictionanry for specific data)
    # - media items (used to create some Diagnosis)
    fixtures = [
        "commons/tests/fixtures/test_nomenclatures.xml",
        "commons/tests/fixtures/test_media.xml",
    ]

    def setUp(self):
        # create client with authentified user
        self.user = createTestUser(
            "user", "password", "add_point", "add_operation"
        )
        self.authentified_client = logTestUser("user", "password")

        # Gather data from DB to create Diagnosis
        owner_id = Nomenclature.objects.filter(type__mnemonic="owner")[0].id

        self.risk_id = Nomenclature.objects.filter(
            type__mnemonic="risk_level"
        )[0].id
        self.eqmtTypeList = Nomenclature.objects.filter(
            type__mnemonic="equipment_type"
        )
        self.eqmtTypeIdList = [
            eqmtType.id for eqmtType in self.eqmtTypeList
        ]  # Gather list of pole type Id
        self.mediaList = Media.objects.all()
        self.mediaIdList = [
            media.id for media in self.mediaList
        ]  # Gather list of media Id

        # create new Point
        data = {
            "owner_id": owner_id,
            "geom": {"type": "Point", "coordinates": [0.5, 0.5]},
        }
        resp = self.authentified_client.post(
            "/api/v1/cables/points/", data, format="json"
        )
        self.assertEqual(resp.status_code, 201)
        self.point_id = resp.json()["properties"]["id"]  # get Point id

    def test_create_first_Operation_with_last_TRUE(self):
        data = {
            "infrastructure": self.point_id,
            "date": "2022-01-01",
            "remark": "My remark",
            "eqmt_type_id": self.eqmtTypeIdList,
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )

        self.assertEqual(resp.status_code, 201)
        # check value
        op = resp.json()
        self.assertTrue(op["last"])

    def test_create_2_Operations_with_last_TRUE_for_newer_FALSE_for_older(
        self,
    ):
        data = {
            "infrastructure": self.point_id,
            "date": "2022-01-01",
            "remark": "My remark",
            "eqmt_type_id": self.eqmtTypeIdList,
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )
        self.assertEqual(resp.status_code, 201)

        # check value for created Operation
        first = resp.json()
        first_id = first["id"]
        self.assertTrue(first["last"])

        # created new Operation on same infrastructure
        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )

        self.assertEqual(resp.status_code, 201)
        # check value for new created Operation
        second = resp.json()
        self.assertTrue(second["last"])
        # check value for old one
        first = Operation.objects.get(id=first_id)
        self.assertFalse(first.last)

    def test_create_2_Operation_containing_Media_with_last_TRUE_for_newer_FALSE_for_older(
        self,
    ):
        data = {
            "infrastructure": self.point_id,
            "date": "2022-01-01",
            "remark": "My remark",
            "eqmt_type_id": self.eqmtTypeIdList,
            "media_id": self.mediaIdList,
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )

        self.assertEqual(resp.status_code, 201)

        # check value for created Operation
        first = resp.json()
        first_id = first["id"]
        self.assertTrue(first["last"])

        # Gather id of pole type list from created Operation and compare to self.poletypeIdList
        eqmtType_check = [eqmtType["id"] for eqmtType in first["eqmt_type"]]
        self.assertListEqual(self.eqmtTypeIdList, eqmtType_check)

        # Gather id of media list from created Operation and compare to self.mediaIdList
        media_check = [media["id"] for media in first["media"]]
        self.assertListEqual(self.mediaIdList, media_check)

        # created new Operation on same infrastructure
        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )

        self.assertEqual(resp.status_code, 201)
        # check value for new created Operation
        second = resp.json()
        self.assertTrue(second["last"])
        # check value for old one
        first = Operation.objects.get(id=first_id)
        self.assertFalse(first.last)

    def test_create_Operation_without_EquimentType__should_fail__(self):
        data = {
            "infrastructure": self.point_id,
            "date": "2022-01-01",
            "remark": "My remark",
            "media_id": self.mediaIdList,
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )
        # check creation fail with statut code 400
        self.assertEqual(resp.status_code, 400)

    def test_create_third_Operation_and_2_first_with_last_TRUE___should_not_occure___(
        self,
    ):
        data = {
            "infrastructure": self.point_id,
            "date": "2022-01-01",
            "remark": "My remark",
            "eqmt_type_id": self.eqmtTypeIdList,
        }
        range_len = 2
        # create 2 Operations on same infrastructure
        for _i in range(0, range_len):
            resp = self.authentified_client.post(
                "/api/v1/cables/operations/", data, format="json"
            )
            self.assertEqual(resp.status_code, 201)
            # check value
            op = resp.json()
            self.assertEqual(op["last"], True)

        # set last=True for all Operations
        Operation.objects.update(infrastructure=self.point_id, last=True)
        # check both Operation with last=True
        ops = Operation.objects.filter(infrastructure=self.point_id, last=True)
        self.assertEqual(len(ops), range_len)

        # create third operation on same infrastructure
        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )
        self.assertEqual(resp.status_code, 201)  # check success
        # check last one created with lat=True
        new = resp.json()
        self.assertTrue(new["last"])
        # check only one is last=True, 2 have last=False
        ops = Operation.objects.filter(
            infrastructure=self.point_id, last=False
        )
        self.assertEqual(len(ops), 2)
        ops = Operation.objects.filter(infrastructure=self.point_id, last=True)
        self.assertEqual(len(ops), 1)


class CreateLineOperationTestCase(TestCase):
    """Class to test creation of Operation related to Line infrastructure.
    This test case mainly focuses on automatic following specific function:
    When first Operation is created from an infrastructure, it has last=True.
    When another one is created for this same infrastructure, the old one is set with last=False and the new one with last=True

    Require creation and consultation of various elements
    """

    # fixture includes:
    # - sinp_nomenclature items (stand for dictionanry for specific data)
    # - media items (used to create some Diagnosis)
    fixtures = [
        "commons/tests/fixtures/test_nomenclatures.xml",
        "commons/tests/fixtures/test_media.xml",
    ]

    def setUp(self):
        # create client with authentified user
        self.user = createTestUser(
            "user", "password", "add_line", "add_operation"
        )
        self.authentified_client = logTestUser("user", "password")

        # Gather data from DB to create Diagnosis
        owner_id = Nomenclature.objects.filter(type__mnemonic="owner")[0].id

        self.risk_id = Nomenclature.objects.filter(
            type__mnemonic="risk_level"
        )[0].id
        self.eqmtTypeList = Nomenclature.objects.filter(
            type__mnemonic="equipment_type"
        )
        self.eqmtTypeIdList = [
            eqmtType.id for eqmtType in self.eqmtTypeList
        ]  # Gather list of pole type Id
        self.mediaList = Media.objects.all()
        self.mediaIdList = [
            media.id for media in self.mediaList
        ]  # Gather list of media Id

        # create new Line
        data = {
            "owner_id": owner_id,
            "geom": {"type": "LineString", "coordinates": [[2, 6], [2, 4]]},
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/lines/", data, format="json"
        )
        self.assertEqual(resp.status_code, 201)
        self.line_id = resp.json()["properties"]["id"]  # get Line id

    def test_create_first_Operation_with_last_TRUE(self):
        # create Operation
        data = {
            "infrastructure": self.line_id,
            "date": "2022-01-01",
            "remark": "My remark",
            "eqmt_type_id": self.eqmtTypeIdList,
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )

        self.assertEqual(resp.status_code, 201)
        # check value
        op = resp.json()
        self.assertTrue(op["last"])

    def test_create_2_Operations_with_last_TRUE_for_newer_FALSE_for_older(
        self,
    ):
        data = {
            "infrastructure": self.line_id,
            "date": "2022-01-01",
            "remark": "My remark",
            "eqmt_type_id": self.eqmtTypeIdList,
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )
        self.assertEqual(resp.status_code, 201)

        # check value for created Operation
        first = resp.json()
        first_id = first["id"]
        self.assertTrue(first["last"])

        # created new Operation on same infrastructure
        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )

        self.assertEqual(resp.status_code, 201)
        # check value for new created Operation
        second = resp.json()
        self.assertTrue(second["last"])
        # check value for old one
        first = Operation.objects.get(id=first_id)
        self.assertFalse(first.last)

    def test_create_2_Operation_containing_Media_with_last_TRUE_for_newer_FALSE_for_older(
        self,
    ):
        data = {
            "infrastructure": self.line_id,
            "date": "2022-01-01",
            "remark": "My remark",
            "eqmt_type_id": self.eqmtTypeIdList,
            "media_id": self.mediaIdList,
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )

        self.assertEqual(resp.status_code, 201)

        # check value for created Operation
        first = resp.json()
        first_id = first["id"]
        self.assertTrue(first["last"])

        # Gather id of pole type list from created Operation and compare to self.poletypeIdList
        eqmtType_check = [eqmtType["id"] for eqmtType in first["eqmt_type"]]
        self.assertListEqual(self.eqmtTypeIdList, eqmtType_check)

        # Gather id of media list from created Operation and compare to self.mediaIdList
        media_check = [media["id"] for media in first["media"]]
        self.assertListEqual(self.mediaIdList, media_check)

        # created new Operation on same infrastructure
        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )

        self.assertEqual(resp.status_code, 201)
        # check value for new created Operation
        second = resp.json()
        self.assertTrue(second["last"])
        # check value for old one
        first = Operation.objects.get(id=first_id)
        self.assertFalse(first.last)

    def test_create_Operation_without_EquimentType__should_fail__(self):
        data = {
            "infrastructure": self.line_id,
            "date": "2022-01-01",
            "remark": "My remark",
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )
        # check creation fail with statut code 400
        self.assertEqual(resp.status_code, 400)

    def test_create_third_Operation_and_2_first_with_last_TRUE___should_not_occure___(
        self,
    ):
        data = {
            "infrastructure": self.line_id,
            "date": "2022-01-01",
            "remark": "My remark",
            "eqmt_type_id": self.eqmtTypeIdList,
        }

        # create 2 Operations on same infrastructure
        for i in range(0, 2):
            resp = self.authentified_client.post(
                "/api/v1/cables/operations/", data, format="json"
            )
            self.assertEqual(resp.status_code, 201)
            # check value
            op = resp.json()
            self.assertEqual(op["last"], True)

        # set last=True for all Operations
        Operation.objects.update(infrastructure=self.line_id, last=True)
        # check both Operation with last=True
        ops = Operation.objects.filter(infrastructure=self.line_id, last=True)
        self.assertEqual(len(ops), 2)

        # create third operation on same infrastructure
        resp = self.authentified_client.post(
            "/api/v1/cables/operations/", data, format="json"
        )
        self.assertEqual(resp.status_code, 201)  # check success
        # check last one created with lat=True
        new = resp.json()
        self.assertTrue(new["last"])
        # check only one is last=True, 2 have last=False
        ops = Operation.objects.filter(infrastructure=self.line_id, last=False)
        self.assertEqual(len(ops), 2)
        ops = Operation.objects.filter(infrastructure=self.line_id, last=True)
        self.assertEqual(len(ops), 1)
