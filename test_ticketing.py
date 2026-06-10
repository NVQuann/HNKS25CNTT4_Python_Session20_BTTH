import unittest
from main import calculate_total_revenue


class TestRevenue(unittest.TestCase):
    def test_booked_and_cancelled_tickets(self):

        tickets = [
            {
                "price": 500,
                "status": "Booked"
            },
            {
                "price": 300,
                "status": "Cancelled"
            },
            {
                "price": 200,
                "status": "Booked"
            }
        ]

        self.assertEqual(
            calculate_total_revenue(tickets),
            700.0
        )

    def test_empty_ticket_list(self):

        tickets = []

        self.assertEqual(
            calculate_total_revenue(tickets),
            0.0
        )


if __name__ == "__main__":
    unittest.main()