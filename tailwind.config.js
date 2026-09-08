/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sunset: {
          bg: '#FFF5ED',
          card: '#FFFCF9',
          cardMuted: '#FFF0E4',
          border: '#FFD6C2',
          borderBlue: '#D2EDFA',
          blush: '#F9E4EE',
          twilight: '#E5F3FC',
          apricot: '#FFD4BF',
          peach: '#FFB38A',
          coral: '#F29363',
          dusk: '#D9713C'
        },
        sky: {
          light: '#DDF4FC',
          DEFAULT: '#8FD3F4',
          deep: '#4FA9D8',
          dark: '#2688BC',
        },
        peach: {
          light: '#FFE0D0',
          DEFAULT: '#FFB38A',
          deep: '#F29363',
          dark: '#D9713C',
        },
        cream: {
          DEFAULT: '#FFF5ED',
          light: '#FFF9F5',
          dark: '#FDEAE1',
        },
        surface: {
          bg: '#FFF5ED',
          card: '#FFFCF9',
          cardMuted: '#FFF0E4',
          border: '#FFD6C2',
          hover: '#FFE8D9',
        },
        brand: {
          text: '#17324D',
          muted: '#60788A',
          subtle: '#8EA4B5',
        },
        command: {
          bg: '#FFF5ED',
          card: '#FFFCF9',
          cardMuted: '#FFF0E4',
          border: '#FFD6C2',
          hover: '#FFE8D9',
          cyan: '#4FA9D8',
          emerald: '#3DB89F',
          amber: '#FFB38A',
          rose: '#F28B82',
          crimson: '#E06A60',
          purple: '#7E9BF2'
        },
        heat: {
          low: '#3DB89F',
          moderate: '#8FD3F4',
          high: '#FFB38A',
          extreme: '#F29363',
          critical: '#E06A60'
        }
      },
      fontFamily: {
        sans: ['Inter', 'Outfit', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace']
      },
      boxShadow: {
        'soft': '0 3px 14px rgba(255, 150, 105, 0.08), 0 1px 3px rgba(79, 169, 216, 0.06)',
        'soft-md': '0 6px 22px rgba(255, 150, 105, 0.1), 0 2px 6px rgba(79, 169, 216, 0.08)',
        'soft-lg': '0 12px 34px rgba(255, 150, 105, 0.12), 0 4px 12px rgba(79, 169, 216, 0.1)',
        'glow-sunset': '0 0 24px -2px rgba(255, 179, 138, 0.4), 0 0 12px -2px rgba(143, 211, 244, 0.3)',
        'glow-sky': '0 0 20px -3px rgba(143, 211, 244, 0.45)',
        'glow-peach': '0 0 20px -3px rgba(255, 179, 138, 0.45)',
        'glow-cyan': '0 0 20px -5px rgba(79, 169, 216, 0.3)',
        'glow-rose': '0 0 20px -5px rgba(242, 147, 99, 0.35)',
        'glow-emerald': '0 0 20px -5px rgba(61, 184, 159, 0.3)',
        'glow-amber': '0 0 20px -5px rgba(255, 179, 138, 0.3)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.3s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(4px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
