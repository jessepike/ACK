---
type: artifact
stage: setup
artifact: testing
description: "Test strategy and configuration (support artifact)"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - Testing Strategy

## Purpose

<!-- Document testing approach and configuration -->

This document captures the testing strategy, tooling, and configuration for [Project Name].

**Testing framework:** [Vitest / Jest / Mocha / etc.]

**Coverage target:** [X]%

---

## Testing Overview

### Test Pyramid

```
          ┌─────────┐
          │   E2E   │  Few, slow, high confidence
          ├─────────┤
          │ Integr- │  Some, medium speed
          │  ation  │
          ├─────────┤
          │  Unit   │  Many, fast, isolated
          └─────────┘
```

### Test Types

| Type | Purpose | Tools | Coverage |
|------|---------|-------|----------|
| Unit | Test individual functions/components | [Tool] | [X]% |
| Integration | Test module interactions | [Tool] | [X]% |
| E2E | Test complete user flows | [Tool] | Critical paths |
| API | Test HTTP endpoints | [Tool] | All endpoints |

---

## Test Configuration

### Vitest/Jest Configuration

**File:** `vitest.config.ts` or `jest.config.js`

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node', // or 'jsdom' for frontend
    include: ['src/**/*.test.ts', 'tests/**/*.test.ts'],
    exclude: ['node_modules', 'dist'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
    setupFiles: ['./tests/setup.ts'],
  },
});
```

### Test Setup File

**File:** `tests/setup.ts`

```typescript
// Global test setup

import { beforeAll, afterAll, beforeEach } from 'vitest';

// Setup test database
beforeAll(async () => {
  // Initialize test environment
});

// Cleanup after tests
afterAll(async () => {
  // Clean up resources
});

// Reset state between tests
beforeEach(() => {
  // Reset mocks, clear data
});
```

---

## Test Directory Structure

```
tests/
├── unit/                    # Unit tests
│   ├── lib/                 # Library function tests
│   │   ├── errors.test.ts
│   │   └── logger.test.ts
│   ├── utils/               # Utility tests
│   │   └── helpers.test.ts
│   └── services/            # Service tests
│       └── user.test.ts
├── integration/             # Integration tests
│   ├── api/                 # API integration tests
│   │   └── users.test.ts
│   └── db/                  # Database integration tests
│       └── queries.test.ts
├── e2e/                     # End-to-end tests
│   ├── auth.test.ts
│   └── user-flows.test.ts
├── fixtures/                # Test data
│   ├── users.ts
│   └── products.ts
├── mocks/                   # Mock implementations
│   ├── db.ts
│   └── services.ts
├── helpers/                 # Test utilities
│   └── test-utils.ts
└── setup.ts                 # Global setup
```

---

## Unit Testing

### Unit Test Pattern

**File:** `tests/unit/lib/errors.test.ts`

```typescript
import { describe, it, expect } from 'vitest';
import { AppError, ValidationError, NotFoundError } from '@/lib/errors';

describe('AppError', () => {
  it('should create error with message and code', () => {
    const error = new AppError('Something went wrong', 'INTERNAL_ERROR');

    expect(error.message).toBe('Something went wrong');
    expect(error.code).toBe('INTERNAL_ERROR');
    expect(error.statusCode).toBe(500);
  });

  it('should accept custom status code', () => {
    const error = new AppError('Bad request', 'BAD_REQUEST', 400);

    expect(error.statusCode).toBe(400);
  });
});

describe('ValidationError', () => {
  it('should include field errors', () => {
    const error = new ValidationError('Invalid input', {
      email: 'Invalid email format',
      name: 'Name is required',
    });

    expect(error.fields).toEqual({
      email: 'Invalid email format',
      name: 'Name is required',
    });
    expect(error.statusCode).toBe(400);
  });
});
```

### What to Unit Test

| Category | Test Focus | Priority |
|----------|------------|----------|
| Pure functions | Input/output, edge cases | High |
| Business logic | Rules, calculations | High |
| Utilities | Helper functions | Medium |
| Validators | Valid/invalid inputs | High |
| Error handling | Error paths | Medium |

---

## Integration Testing

### API Integration Test Pattern

**File:** `tests/integration/api/users.test.ts`

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createTestApp } from '@/tests/helpers/test-utils';
import { db } from '@/lib/db';

describe('Users API', () => {
  let app: ReturnType<typeof createTestApp>;

  beforeAll(async () => {
    app = await createTestApp();
    await db.user.deleteMany(); // Clean state
  });

  afterAll(async () => {
    await db.$disconnect();
  });

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const response = await app.request('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: 'test@example.com',
          name: 'Test User',
        }),
      });

      expect(response.status).toBe(201);
      const data = await response.json();
      expect(data.user.email).toBe('test@example.com');
    });

    it('should reject invalid email', async () => {
      const response = await app.request('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: 'invalid-email',
          name: 'Test User',
        }),
      });

      expect(response.status).toBe(400);
    });
  });

  describe('GET /api/users/:id', () => {
    it('should return user by ID', async () => {
      // Create user first
      const user = await db.user.create({
        data: { email: 'get@example.com', name: 'Get Test' },
      });

      const response = await app.request(`/api/users/${user.id}`);

      expect(response.status).toBe(200);
      const data = await response.json();
      expect(data.user.id).toBe(user.id);
    });

    it('should return 404 for non-existent user', async () => {
      const response = await app.request('/api/users/non-existent-id');

      expect(response.status).toBe(404);
    });
  });
});
```

### Database Integration Test Pattern

**File:** `tests/integration/db/queries.test.ts`

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { db } from '@/lib/db';
import { UserService } from '@/services/user';

describe('UserService database operations', () => {
  const userService = new UserService();

  beforeEach(async () => {
    await db.user.deleteMany();
  });

  it('should find users with pagination', async () => {
    // Create test users
    await db.user.createMany({
      data: [
        { email: 'user1@test.com', name: 'User 1' },
        { email: 'user2@test.com', name: 'User 2' },
        { email: 'user3@test.com', name: 'User 3' },
      ],
    });

    const result = await userService.findAll({ page: 1, pageSize: 2 });

    expect(result.data).toHaveLength(2);
    expect(result.pagination.total).toBe(3);
    expect(result.pagination.totalPages).toBe(2);
  });
});
```

---

## E2E Testing

### E2E Test Pattern (Playwright)

**File:** `tests/e2e/auth.test.ts`

```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('user can sign up and log in', async ({ page }) => {
    // Navigate to signup
    await page.goto('/signup');

    // Fill signup form
    await page.fill('[name="email"]', 'newuser@test.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.fill('[name="confirmPassword"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    // Verify redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');

    // Log out
    await page.click('[data-testid="logout-button"]');
    await expect(page).toHaveURL('/login');

    // Log back in
    await page.fill('[name="email"]', 'newuser@test.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    // Verify login successful
    await expect(page).toHaveURL('/dashboard');
  });

  test('shows error for invalid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'wrong@test.com');
    await page.fill('[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    await expect(page.locator('[role="alert"]')).toContainText('Invalid credentials');
  });
});
```

### Playwright Configuration

**File:** `playwright.config.ts`

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## Mocking

### Mock Patterns

**File:** `tests/mocks/db.ts`

```typescript
import { vi } from 'vitest';

export const mockDb = {
  user: {
    findUnique: vi.fn(),
    findMany: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  },
  // Add other models
};

// Reset all mocks
export const resetMocks = () => {
  Object.values(mockDb).forEach((model) => {
    Object.values(model).forEach((fn) => {
      if (typeof fn.mockReset === 'function') {
        fn.mockReset();
      }
    });
  });
};
```

### Using Mocks

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mockDb, resetMocks } from '@/tests/mocks/db';
import { UserService } from '@/services/user';

vi.mock('@/lib/db', () => ({ db: mockDb }));

describe('UserService', () => {
  beforeEach(() => {
    resetMocks();
  });

  it('should find user by email', async () => {
    mockDb.user.findUnique.mockResolvedValue({
      id: '1',
      email: 'test@example.com',
      name: 'Test',
    });

    const service = new UserService();
    const user = await service.findByEmail('test@example.com');

    expect(user).not.toBeNull();
    expect(mockDb.user.findUnique).toHaveBeenCalledWith({
      where: { email: 'test@example.com' },
    });
  });
});
```

---

## Test Fixtures

**File:** `tests/fixtures/users.ts`

```typescript
export const testUsers = {
  admin: {
    id: 'user-admin-1',
    email: 'admin@test.com',
    name: 'Admin User',
    role: 'admin' as const,
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-01'),
  },
  regular: {
    id: 'user-regular-1',
    email: 'user@test.com',
    name: 'Regular User',
    role: 'user' as const,
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-01'),
  },
};

export const createUserFixture = (overrides = {}) => ({
  id: 'user-' + Math.random().toString(36).substr(2, 9),
  email: `user-${Date.now()}@test.com`,
  name: 'Test User',
  role: 'user' as const,
  createdAt: new Date(),
  updatedAt: new Date(),
  ...overrides,
});
```

---

## NPM Scripts

**File:** `package.json`

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui",
    "test:unit": "vitest run tests/unit",
    "test:integration": "vitest run tests/integration",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  }
}
```

---

## Coverage Requirements

### Thresholds

| Metric | Minimum | Target |
|--------|---------|--------|
| Lines | 80% | 90% |
| Functions | 80% | 90% |
| Branches | 80% | 85% |
| Statements | 80% | 90% |

### Coverage Exclusions

Files excluded from coverage:
- Configuration files (`*.config.*`)
- Type definitions (`*.d.ts`)
- Test files (`*.test.*`, `*.spec.*`)
- Generated code (`/generated/`)

---

## Testing Checklist

### Setup Complete

- [ ] Test framework installed and configured
- [ ] Test directory structure created
- [ ] Setup files in place
- [ ] NPM scripts configured

### Test Coverage

- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] Integration tests for database operations
- [ ] E2E tests for critical paths

### CI Integration

- [ ] Tests run in CI pipeline
- [ ] Coverage reports generated
- [ ] Coverage thresholds enforced

---

## Related Documents

- [ci-cd.md](ci-cd.md) - CI/CD pipeline
- [scaffolding.md](scaffolding.md) - Code structure
- [architecture.md](../design/templates/architecture.md) - System design
