import unittest
from backtester import Backtester
import pandas as pd
import os

class TestBacktester(unittest.TestCase):
    def test_backtest_run(self):
        # Use a short period to make it fast
        print("\nTesting Backtester with AAPL (1mo)...")
        bt = Backtester("AAPL", period="1mo")
        bt.load_data()
        
        # Check data loading
        self.assertFalse(bt.data.empty, "Data should not be empty")
        self.assertIn("rsi", bt.data.columns, "RSI should be calculated")
        self.assertIn("movement_score", bt.data.columns, "Movement score should be calculated")
        
        # Run simulation
        bt.run(mode="llm")
        
        # Check results
        metrics = bt.calculate_metrics()
        print("Metrics:", metrics)
        
        self.assertIn("Total Return (%)", metrics)
        self.assertIn("Sharpe Ratio", metrics)
        self.assertIn("Max Drawdown (%)", metrics)
        
        # Check if history is populated
        self.assertTrue(len(bt.history) > 0, "History should be populated")
        
        # Check if trades list exists (might be empty if no trades triggered, but list should exist)
        self.assertIsInstance(bt.trades, list)

        # Test Plotting
        plot_filename = "test_backtest_plot.png"
        if os.path.exists(plot_filename):
            os.remove(plot_filename)
            
        bt.plot_results(filename=plot_filename)
        self.assertTrue(os.path.exists(plot_filename), "Plot file should be created")
        print(f"Plot verified: {plot_filename}")
        
        # Clean up
        if os.path.exists(plot_filename):
            os.remove(plot_filename)

if __name__ == "__main__":
    unittest.main()
