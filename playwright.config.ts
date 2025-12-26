import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI
    ? [['list'], ['json', { outputFile: 'test-results.json' }]]
    : [['html', { open: 'never' }], ['list']],
  use: {
    baseURL: process.env.CI ? 'http://localhost:4321' : 'http://localhost:9103',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: process.env.CI ? 'npx astro preview --port 4321' : 'npm run dev',
    url: process.env.CI ? 'http://localhost:4321' : 'http://localhost:9103',
    reuseExistingServer: !process.env.CI,
    timeout: 60 * 1000,
  },
});
