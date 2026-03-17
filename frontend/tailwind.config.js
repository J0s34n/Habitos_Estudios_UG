/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
        colors: {
          'azul-oscuro': '#0a1628',
          'azul-medio': '#0d2a5c',
          'azul-claro': '#1a4a9f',
          'arena': '#c9a96e',
        }
    },
  },
  plugins: [],
}

