/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        fintech: {
          bg: '#0B0B0C',        // Background Black
          panel: '#131316',     // Dark Panel
          card: '#1A1A1E',      // Elevated Card
          border: '#2A2A2E',    // Card Border
          primary: '#8A2BE2',   // Electric Purple
          primaryHover: '#7A23D8',
          textMain: '#FFFFFF',
          textSec: '#B9B9C9',
          bull: '#3BE28F',      // Green
          bear: '#FF4F6F',      // Red
          neutral: '#F5C542',   // Yellow
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Ensure you import Inter in your CSS
      },
      boxShadow: {
        'glow-purple': '0 0 15px rgba(138, 43, 226, 0.15)',
        'glow-green': '0 0 15px rgba(59, 226, 143, 0.15)',
        'glow-red': '0 0 15px rgba(255, 79, 111, 0.15)',
      }
    },
  },
  plugins: [],
}