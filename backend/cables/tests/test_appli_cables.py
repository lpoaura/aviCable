from django.contrib.gis.geos import MultiPolygon, Polygon
from django.test import TestCase
from sinp_nomenclatures.models import Nomenclature

from commons.tests.tests_commons import createTestUser, logTestUser
from geo_area.models import GeoArea


class CreatePointAndLineTestCase(TestCase):
    """Class to test creation Point and Line.
    This test case mainly focuses on automatic attachment of GeoAreas and SensitiveAreas that are geographically correlated with the infrastructures (Point/Line)

    Require creation and consultation of various elements
    """

    # - It contains needed sinp_nomenclature items (stand for dictionanry for specific data)
    fixtures = ["commons/tests/fixtures/test_nomenclatures.xml"]

    def setUp(self):
        # create client with authentified user
        self.user = createTestUser(
            "user", "password", "add_sensitivearea", "add_point", "add_line"
        )
        self.authentified_client = logTestUser("user", "password")

        # CREATE 2 SENSITIVE_AREA
        data = {
            "name": "Zone Sensible 1",
            "code": "ZS1",
            "geom": {
                "type": "Polygon",
                "coordinates": [[[0, 5], [0, -5], [5, -5], [5, 5], [0, 5]]],
            },
        }
        self.authentified_client.post(
            "/api/v1/sensitive-areas/", data, format="json"
        )
        data = {
            "name": "Zone Sensible 2",
            "code": "ZS2",
            "geom": {
                "type": "Polygon",
                "coordinates": [[[-1, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]]],
            },
        }
        self.authentified_client.post(
            "/api/v1/sensitive-areas/", data, format="json"
        )

        # CREATE 2 GEO_AREA
        # get id of a geoarea type in nomanclature (the first one)
        ga_type = (
            Nomenclature.objects.all()
            .filter(type__mnemonic="geoarea_type")[0]
            .id
        )
        # create 2 GeoArea (no request as post method was not implemented: not to be created by
        # users but directly from DB)
        ga = GeoArea.objects.create(
            type_id=ga_type,
            name="Geo Area 1",
            code="GA1",
            geom=MultiPolygon(
                Polygon(((-5, 5), (-5, -5), (5, -5), (5, 5), (-5, 5)))
            ),
        )
        ga.save()
        ga = GeoArea.objects.create(
            type_id=ga_type,
            name="Geo Area 2",
            code="GA2",
            geom=MultiPolygon(
                Polygon(((-1, 1), (-1, -1), (1, -1), (1, 1), (-1, 1)))
            ),
        )
        ga.save()

    def test_create_and_get_point_inside_2SA_and_2GA(self):
        # TEST POINT
        # Create 4 Points:
        # - one inside both SensitiveArea and both GeoArea
        data = {
            "owner_id": 1,
            "geom": {"type": "Point", "coordinates": [0.5, 0.5]},
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/points/", data, format="json"
        )
        self.assertEquals(resp.status_code, 201)
        # method get tested: get one specific Point
        points = resp.json()
        id = points["properties"]["id"]
        resp = self.authentified_client.get(f"/api/v1/cables/points/{id}/")
        self.assertEquals(resp.status_code, 200)
        point = resp.json()
        self.assertEquals(len(point["properties"]["sensitive_area"]), 2)
        self.assertEquals(len(point["properties"]["areas"]), 2)

    def test_create_and_get_point_inside_1SA_and_2GA(self):
        # - one outside one SensitiveArea and inside both GeoArea
        data = {
            "owner_id": 1,
            "geom": {"type": "Point", "coordinates": [-0.5, 0.5]},
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/points/", data, format="json"
        )
        self.assertEquals(resp.status_code, 201)
        # method get tested: get one specific Point
        points = resp.json()
        id = points["properties"]["id"]
        resp = self.authentified_client.get(f"/api/v1/cables/points/{id}/")
        self.assertEquals(resp.status_code, 200)
        point = resp.json()
        self.assertEquals(len(point["properties"]["sensitive_area"]), 1)
        self.assertEquals(len(point["properties"]["areas"]), 2)

    def test_create_and_get_point_outside_all_SA_and_GA(self):
        # - one outside both SensitiveArea and both GeoArea
        data = {
            "owner_id": 1,
            "geom": {"type": "Point", "coordinates": [10, 10]},
        }
        resp = self.authentified_client.post(
            "/api/v1/cables/points/", data, format="json"
        )
        self.assertEquals(resp.status_code, 201)
        # method get tested: get one specific Point
        points = resp.json()
        id = points["properties"]["id"]
        resp = self.authentified_client.get(f"/api/v1/cables/points/{id}/")
        self.assertEquals(resp.status_code, 200)
        point = resp.json()
        self.assertEquals(len(point["properties"]["sensitive_area"]), 0)
        self.assertEquals(len(point["properties"]["areas"]), 0)

    def test_create_and_get_point_at_limit_of_1SA_and_1GA(self):
        # same test with values at the limit:
        # => inside one SensitiveArea and one GeoArea
        data = {
            "owner_id": 1,
            "geom": {"type": "Point", "coordinates": [5, 5]},
        }
        resp = self.authentified_client.post(
            "/api/v1/cables/points/", data, format="json"
        )
        self.assertEquals(resp.status_code, 201)
        # method get tested: get one specific Point
        points = resp.json()
        id = points["properties"]["id"]
        resp = self.authentified_client.get(f"/api/v1/cables/points/{id}/")
        self.assertEquals(resp.status_code, 200)
        point = resp.json()
        self.assertEquals(len(point["properties"]["sensitive_area"]), 1)
        self.assertEquals(len(point["properties"]["areas"]), 1)

    def test_create_and_get_point_list(self):
        # test get list: create several points (nb)
        data = {
            "owner_id": 1,
            "geom": {"type": "Point", "coordinates": [5, 5]},
        }
        nb = 4
        for i in range(0, nb):
            resp = self.authentified_client.post(
                "/api/v1/cables/points/", data, format="json"
            )
            self.assertEquals(resp.status_code, 201)

        resp = self.authentified_client.get("/api/v1/cables/points/")
        self.assertEquals(resp.status_code, 200)
        points = resp.json()
        self.assertEquals(len(points["features"]), nb)

    def test_create_and_get_line_inside_2SA_and_2GA(self):
        # TEST LINE
        # Create 4 Lines:
        # - one entirely inside both SensitiveArea and both GeoArea
        data = {
            "owner_id": 1,
            "geom": {
                "type": "LineString",
                "coordinates": [[-0.5, -0.5], [0.5, 0.5]],
            },
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/lines/", data, format="json"
        )
        self.assertEquals(resp.status_code, 201)

        # method get tested: get one specific Line
        lines = resp.json()

        id = lines["properties"]["id"]

        resp = self.authentified_client.get(f"/api/v1/cables/lines/{id}/")
        self.assertEquals(resp.status_code, 200)
        line = resp.json()

        self.assertEquals(len(line["properties"]["sensitive_area"]), 2)
        self.assertEquals(len(line["properties"]["areas"]), 2)

    def test_create_and_get_line_inside_1SA_and_2GA(self):
        # - one outside one SensitiveArea and inside both GeoArea
        data = {
            "owner_id": 1,
            "geom": {
                "type": "LineString",
                "coordinates": [[-2, 2], [-0.5, 0.5]],
            },
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/lines/", data, format="json"
        )
        self.assertEquals(resp.status_code, 201)

        # method get tested: get one specific Line
        lines = resp.json()

        id = lines["properties"]["id"]
        resp = self.authentified_client.get(f"/api/v1/cables/lines/{id}/")
        self.assertEquals(resp.status_code, 200)

        line = resp.json()
        self.assertEquals(len(line["properties"]["sensitive_area"]), 1)
        self.assertEquals(len(line["properties"]["areas"]), 2)

    def test_create_and_get_line_outside_all_SA_and_GA(self):
        # - one outside both SensitiveArea and both GeoArea
        data = {
            "owner_id": 1,
            "geom": {"type": "LineString", "coordinates": [[-6, 6], [-6, -6]]},
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/lines/", data, format="json"
        )
        self.assertEquals(resp.status_code, 201)

        # method get tested: get one specific Line
        lines = resp.json()

        id = lines["properties"]["id"]
        resp = self.authentified_client.get(f"/api/v1/cables/lines/{id}/")
        self.assertEquals(resp.status_code, 200)
        line = resp.json()

        self.assertEquals(len(line["properties"]["sensitive_area"]), 0)
        self.assertEquals(len(line["properties"]["areas"]), 0)

    def test_create_and_get_line_intersecting_1SA_and_1GA(self):
        # same test with line intersecting the areas:
        # => inside one SensitiveArea and one GeoArea
        data = {
            "owner_id": 1,
            "geom": {"type": "LineString", "coordinates": [[2, 6], [2, 4]]},
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/lines/", data, format="json"
        )
        self.assertEquals(resp.status_code, 201)
        # method get tested: get one specific Line
        lines = resp.json()

        id = lines["properties"]["id"]
        resp = self.authentified_client.get(f"/api/v1/cables/lines/{id}/")
        self.assertEquals(resp.status_code, 200)
        line = resp.json()
        self.assertEquals(len(line["properties"]["sensitive_area"]), 1)
        self.assertEquals(len(line["properties"]["areas"]), 1)

    def test_create_and_get_line_intersecting_with_one_point_only_1SA_and_1GA(
        self,
    ):
        # same test with line  with only one point the areas:
        # => inside one SensitiveArea and one GeoArea
        data = {
            "owner_id": 1,
            "geom": {"type": "LineString", "coordinates": [[2, 6], [2, 5]]},
        }

        resp = self.authentified_client.post(
            "/api/v1/cables/lines/", data, format="json"
        )
        self.assertEquals(resp.status_code, 201)
        # method get tested: get one specific Line
        lines = resp.json()

        id = lines["properties"]["id"]
        resp = self.authentified_client.get(f"/api/v1/cables/lines/{id}/")
        self.assertEquals(resp.status_code, 200)
        line = resp.json()
        self.assertEquals(len(line["properties"]["sensitive_area"]), 1)
        self.assertEquals(len(line["properties"]["areas"]), 1)

    def test_create_and_get_line_list(self):
        # test get list: create several lines (nb)
        data = {
            "owner_id": 1,
            "geom": {"type": "LineString", "coordinates": [[-5, -5], [5, 5]]},
        }
        nb = 4
        for i in range(0, nb):
            resp = self.authentified_client.post(
                "/api/v1/cables/lines/", data, format="json"
            )
            self.assertEquals(resp.status_code, 201)

        resp = self.authentified_client.get("/api/v1/cables/lines/")
        self.assertEquals(resp.status_code, 200)
        points = resp.json()
        self.assertEquals(len(points["features"]), nb)
