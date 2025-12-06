export const mockData = {
  user: {
    name: "Alex Sterling",
    totalBalance: 124500.80, // Combined net worth
    currency: "$"
  },
  // NEW: Everyday Banking Data
  banking: {
    checkingBalance: 14250.00,
    savingsBalance: 35000.00,
    cards: [
      { id: 1, type: "Visa Infinite", number: "**** 4829", expiry: "12/28", holder: "ALEX STERLING", color: "purple" },
      { id: 2, type: "Mastercard Black", number: "**** 9921", expiry: "09/26", holder: "ALEX STERLING", color: "black" }
    ],
    recentTransactions: [
      { id: 1, to: "Netflix Subscription", date: "Today, 10:23 AM", amount: -15.99, type: "sub", icon: "🎬" },
      { id: 2, to: "Salary Deposit", date: "Yesterday, 9:00 AM", amount: +4500.00, type: "income", icon: "💰" },
      { id: 3, to: "Uber Rides", date: "Yesterday, 8:45 PM", amount: -24.50, type: "transport", icon: "🚗" },
      { id: 4, to: "Transfer to Savings", date: "Oct 24", amount: -500.00, type: "transfer", icon: "🏦" },
    ]
  },
  // Investment / AI Data
  portfolio: {
    investedValue: 75250.80,
    dayChange: "+1,240.50",
    dayChangePercent: "+1.65%",
    assets: [
      { symbol: "AAPL", name: "Apple Inc.", price: 175.50, change: "+1.2%", sentiment: "Bullish" },
      { symbol: "BTC", name: "Bitcoin", price: 42000.00, change: "-0.5%", sentiment: "Neutral" },
      { symbol: "NVDA", name: "Nvidia", price: 460.00, change: "+3.8%", sentiment: "Bullish" },
    ]
  },
  // ... (Keep the Sentiment/Technical agent data from previous step)
  sentimentAgent: {
    score: 0.75,
    label: "Bullish",
    summary: "Tech sector rallying on AI expectations."
  }
};