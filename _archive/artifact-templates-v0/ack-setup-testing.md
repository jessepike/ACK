---
type: artifact
stage: setup
artifact: testing
description: "Test strategy, configuration, and coverage targets"
version: "1.0.0"
status: draft
---

# [Project Name] - Testing Strategy

## Overview

- **Test Framework:** [Jest / Vitest / Pytest / etc]
- **Coverage Tool:** [Built-in / NYC / Coverage.py / etc]
- **E2E Framework:** [Playwright / Cypress / None]

---

## Testing Pyramid

```
        /\
       /  \      E2E Tests (few)
      /----\     - Critical user journeys
     /      \    - Smoke tests
    /--------\   Integration Tests (some)
   /          \  - API tests
  /            \ - Component integration
 /--------------\
/                \ Unit Tests (many)
 - Functions, utilities
 - Pure business logic
```

---

## Test Categories

### Unit Tests

**Purpose:** Test individual functions and modules in isolation.

**Location:** `[tests/unit/ or __tests__/]`

**Naming:** `[filename].test.[ext]` or `[filename].spec.[ext]`

**Coverage Target:** [X]%

**What to test:**
- [ ] Pure functions
- [ ] Utility helpers
- [ ] Business logic
- [ ] Data transformations

**What NOT to unit test:**
- External API calls (mock these)
- Database operations (integration tests)
- UI rendering (component tests)

### Integration Tests

**Purpose:** Test how components work together.

**Location:** `[tests/integration/]`

**Coverage Target:** [X]%

**What to test:**
- [ ] API endpoint handlers
- [ ] Database operations
- [ ] Service layer interactions
- [ ] Component compositions

### End-to-End (E2E) Tests

**Purpose:** Test critical user journeys through the full application.

**Location:** `[tests/e2e/]`

**Framework:** [Playwright / Cypress / None]

**What to test:**
- [ ] User authentication flow
- [ ] Core feature workflows
- [ ] Critical business processes
- [ ] Payment/checkout (if applicable)

---

## Test Configuration

### Test Runner Config

```javascript
// [config file name - e.g., jest.config.js, vitest.config.ts]
export default {
  // Test file patterns
  testMatch: ['**/*.test.[jt]s?(x)', '**/*.spec.[jt]s?(x)'],

  // Coverage configuration
  collectCoverageFrom: [
    'src/**/*.[jt]s?(x)',
    '!src/**/*.d.ts',
    '!src/**/index.[jt]s',
  ],

  // Coverage thresholds
  coverageThreshold: {
    global: {
      branches: [X],
      functions: [X],
      lines: [X],
      statements: [X],
    },
  },

  // Setup files
  setupFilesAfterEnv: ['[setup-file]'],

  // Module aliases (if using)
  moduleNameMapper: {
    '@/(.*)': '<rootDir>/src/$1',
  },
};
```

### E2E Config (if applicable)

```javascript
// [e2e config file - e.g., playwright.config.ts]
export default {
  testDir: './tests/e2e',
  baseURL: '[http://localhost:3000]',

  use: {
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },

  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    // Add other browsers as needed
  ],
};
```

---

## Coverage Targets

| Category | Target | Current |
|----------|--------|---------|
| Statements | [X]% | - |
| Branches | [X]% | - |
| Functions | [X]% | - |
| Lines | [X]% | - |

### Critical Paths (100% coverage required)

- [ ] [Critical module 1]
- [ ] [Critical module 2]
- [ ] [Authentication logic]
- [ ] [Payment processing]

---

## Test Data Strategy

### Fixtures

**Location:** `[tests/fixtures/]`

```javascript
// Example fixture structure
export const mockUser = {
  id: '[test-id]',
  email: '[test@example.com]',
  // ...
};
```

### Factories (if using)

```javascript
// Example factory
export function createUser(overrides = {}) {
  return {
    id: generateId(),
    email: faker.internet.email(),
    ...overrides,
  };
}
```

### Database Seeding

- **Strategy:** [Fresh DB per test / Transactions / Snapshots]
- **Seed Script:** `[seed command]`

---

## Mocking Strategy

### External Services

| Service | Mock Strategy | Mock Location |
|---------|---------------|---------------|
| [API 1] | [MSW / Manual mock] | `[mocks/]` |
| [Database] | [In-memory / Mock] | `[mocks/]` |
| [Auth Provider] | [Mock] | `[mocks/]` |

### Mock Server (if using MSW or similar)

```javascript
// [mocks/handlers.js]
export const handlers = [
  // Define mock API handlers
];
```

---

## Running Tests

```bash
# Run all tests
[test-command]

# Run with coverage
[test-command] --coverage

# Run specific test file
[test-command] [path/to/test]

# Run tests in watch mode
[test-command] --watch

# Run E2E tests
[e2e-test-command]

# Run E2E in headed mode (debugging)
[e2e-test-command] --headed
```

---

## CI Integration

### Required Checks

- [ ] Unit tests must pass
- [ ] Integration tests must pass
- [ ] Coverage thresholds must be met
- [ ] E2E tests pass (on deploy)

### Test Reporting

- **Unit/Integration:** [Jest HTML report / Vitest UI / etc]
- **Coverage:** [Codecov / Coveralls / Built-in]
- **E2E:** [Playwright report / Cypress dashboard]

---

## Setup Checklist

### Phase 1: Framework Setup
- [ ] Install test framework
- [ ] Create config file
- [ ] Add test scripts to package.json

### Phase 2: First Tests
- [ ] Write first unit test
- [ ] Verify tests run locally
- [ ] Set up test directory structure

### Phase 3: Coverage
- [ ] Enable coverage reporting
- [ ] Set coverage thresholds
- [ ] Add coverage to CI

### Phase 4: E2E (if applicable)
- [ ] Install E2E framework
- [ ] Create E2E config
- [ ] Write first E2E test
- [ ] Add E2E to CI

---

## Open Questions

- [ ] [Testing question 1]
- [ ] [Testing question 2]
