# FinTech Dashboard Frontend

A modern, comprehensive financial technology dashboard built with React, featuring AI-powered investment insights, banking functionality, market analysis, and real-time data visualization.

## 🚀 Features

- **AI Financial Advisor**: Interactive chat interface powered by multi-agent AI system
- **AI Investment Tools**: Intelligent investment recommendations and portfolio analysis
- **Banking Dashboard**: Complete banking interface with account management
- **Money Transfers**: Secure fund transfers between accounts
- **Transaction History**: Detailed transaction tracking and history
- **Market Sentiment Analysis**: Real-time sentiment indicators and market mood analysis
- **Technical Analysis**: Advanced charts and technical indicators for market data
- **User Verification**: Secure user authentication and verification system
- **Responsive Design**: Mobile-first design with modern UI/UX

## 🛠 Tech Stack

- **Frontend Framework**: React 19.2.0
- **Build Tool**: Vite (with Rolldown)
- **Routing**: React Router DOM
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Charts**: Recharts
- **State Management**: React Hooks
- **HTTP Client**: Fetch API

## 📁 Project Structure

```
fintech-dashboard/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Card.jsx        # Card component
│   │   └── Sidebar.jsx     # Navigation sidebar
│   ├── layout/
│   │   └── MainLayout.jsx  # Main application layout
│   ├── pages/              # Page components
│   │   ├── Advisor.jsx     # AI Financial Advisor
│   │   ├── AIInvest.jsx    # AI Investment Tools
│   │   ├── BankingDashboard.jsx # Banking interface
│   │   ├── Dashboard.jsx   # Main dashboard
│   │   ├── History.jsx     # Transaction history
│   │   ├── Sentiment.jsx   # Market sentiment
│   │   ├── Technicals.jsx  # Technical analysis
│   │   ├── Transfer.jsx    # Money transfers
│   │   └── Verification.jsx # User verification
│   ├── data/
│   │   └── mockData.js     # Mock data for development
│   └── assets/             # Static assets
├── public/                 # Public assets
└── dist/                   # Build output (generated)
```

## 🚀 Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend server running (see backend README)

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd fintech-dashboard
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5173` (default Vite port)

### Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint for code quality checks

## 🔧 Configuration

The application connects to a backend API server. Make sure the backend is running on `http://localhost:5000` or update the API endpoints in the components accordingly.

## 🎨 Styling

This project uses Tailwind CSS for styling with custom color schemes:
- Primary: FinTech purple/blue theme
- Dark mode optimized
- Responsive design patterns
- Custom animations and transitions

## 📱 Pages Overview

- **/** - Banking Dashboard (default landing page)
- **/ai-invest** - AI Investment Tools
- **/advisor** - AI Financial Advisor Chat
- **/sentiment** - Market Sentiment Analysis
- **/technicals** - Technical Analysis Charts
- **/transfers** - Money Transfer Interface
- **/history** - Transaction History
- **/verification** - User Verification

## 🔌 API Integration

The frontend communicates with the backend API for:
- Chat functionality with AI Advisor
- Real-time market data
- Transaction processing
- User authentication
- Market sentiment analysis

## 🐛 Development & Debugging

For debugging information, check the `DEBUGGING.md` file in the root directory.

## 📦 Build & Deployment

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Preview production build:**
   ```bash
   npm run preview
   ```

The built files will be in the `dist/` directory, ready for deployment to any static hosting service.

## 🤝 Contributing

1. Follow the existing code style and patterns
2. Run linting before committing: `npm run lint`
3. Test components across different screen sizes
4. Ensure API calls handle errors gracefully

## 📄 License

This project is part of a FinTech dashboard application.
