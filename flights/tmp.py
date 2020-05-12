



    def test_valid_duration(self):
        a = Airport.objects.get(code="AAA")
        b = Airport.objects.get(code="BBB")

        f = Flight.objects.get(origin=a,destination=b,duration=100)

        self.assertFalse(f.is_valid_flight())