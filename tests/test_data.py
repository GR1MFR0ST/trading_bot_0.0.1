import unittest
from data.historical import HistoricalDataFetcher
from config import Config

class TestDataFetching(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.fetcher = HistoricalDataFetcher(self.config)

    def test_get_data(self):
        df = self.fetcher.get_data("EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm", "raydium")
        self.assertFalse(df.empty)

if __name__ == '__main__':
    unittest.main()