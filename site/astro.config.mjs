import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://atebaa-elkheir.example',
  build: { format: 'directory' },
  image: { layout: 'constrained' },
});
