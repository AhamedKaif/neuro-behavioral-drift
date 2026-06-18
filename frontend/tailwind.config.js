/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // High-end medical/cybernetic aesthetic
        darkBg: '#0b0f19',
        darkCard: '#151c2c',
        darkBorder: '#222f47',
        strainLow: '#10b981',    // Emerald
        strainMedium: '#f59e0b', // Amber
        strainHigh: '#ef4444',   // Rose
        accentBlue: '#3b82f6',   // Blue
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow-pulse': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(59, 130, 246, 0.2), 0 0 10px rgba(59, 130, 246, 0.1)' },
          '100%': { boxShadow: '0 0 15px rgba(59, 130, 246, 0.5), 0 0 25px rgba(59, 130, 246, 0.3)' },
        }
      }
    },
  },
  plugins: [],
}
