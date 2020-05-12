from django.db.models import Max
from django.test import Client, TestCase

from.models import Airport,Flight,Passenger

# Create your tests here.
class ModelsTestCase(TestCase):
    def setUp(self):
        a1 = Airport.objects.create(code="AAA",city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        Flight.objects.create(origin=a1,destination=a2,duration=200)
        Flight.objects.create(origin=a1,destination=a1,duration=100)
        Flight.objects.create(origin=a1,destination=a2,duration=-100)

    def test_departure_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(),3)

    def test_arrival_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(),1)

    def test_valid_flight(self):
        a = Airport.objects.get(code="AAA")
        b = Airport.objects.get(code="BBB")

        f = Flight.objects.get(origin=a,destination=b,duration=200)
        self.assertTrue(f.is_valid_flight())
    
    def test_valid_duration(self):
        a = Airport.objects.get(code="AAA")
        b = Airport.objects.get(code="BBB")

        f = Flight.objects.get(origin=a,destination=b,duration=-100)

        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        c = Client()

        response = c.get("/")

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["flights"].count(),3)

    def test_valid_flight_page(self):
        a = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a,destination=a)

        c = Client()

        response = c.get(f"/{f.id}")

        self.assertEqual(response.status_code,200)

    def test_invalid_flight_page(self):
        
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()

        response = c.get(f"/{max_id+1}")

        self.assertEqual(response.status_code,404)


    def test_fight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Rajeevan",last="Aiyadurai")
        f.passengers.add(p)

        c = Client()

        response = c.get(f"/{f.id}")

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["passengers"].count(),1)

    def test_fight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Kishaalyan",last="Rajeevan")

        c = Client()

        response = c.get(f"/{f.id}")

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["non_passengers"].count(),1)