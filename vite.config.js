import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vite.dev/config/
export default defineConfig({
  base: '/kody-james-portfolio/',
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    fs: {
      allow: ['..'],
    },
  },
  assetsInclude: ['**/_*.py'], // Include files starting with underscore
});
