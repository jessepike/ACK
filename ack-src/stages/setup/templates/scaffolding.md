---
type: artifact
stage: setup
artifact: scaffolding
description: "Initial code structure and boilerplate (support artifact)"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - Scaffolding

## Purpose

<!-- Document code scaffolding decisions -->

This document captures the initial code scaffolding for [Project Name], including base components, utilities, and configuration that establish patterns for the codebase.

**Framework:** [From stack.md]

**Scaffolding approach:** [CLI generator / Manual / Hybrid]

---

## Scaffolding Overview

### What Gets Scaffolded

| Category | Items | Purpose |
|----------|-------|---------|
| Config files | [List] | Project configuration |
| Type definitions | [List] | Shared types |
| Base components | [List] | Reusable UI/logic |
| Utilities | [List] | Helper functions |
| API structure | [List] | Endpoint organization |

---

## Configuration Files

### TypeScript Configuration

**File:** `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Key decisions:**
- [Why these compiler options]

---

### Linting Configuration

**File:** `.eslintrc.js` or `eslint.config.js`

```javascript
// ESLint configuration
module.exports = {
  // [Configuration details]
};
```

**File:** `.prettierrc`

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

---

### Environment Configuration

**File:** `src/config/env.ts`

```typescript
// Environment configuration pattern
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']),
  PORT: z.string().transform(Number),
  DATABASE_URL: z.string().url(),
  // Add other env vars
});

export const env = envSchema.parse(process.env);
```

---

## Type Definitions

### Shared Types

**File:** `src/types/index.ts`

```typescript
// Common type definitions

// API Response wrapper
export interface ApiResponse<T> {
  data: T;
  meta?: {
    timestamp: string;
    [key: string]: unknown;
  };
}

// Error response
export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}

// Pagination
export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
  };
}

// [Add project-specific types]
```

### Entity Types

**File:** `src/types/entities.ts`

```typescript
// Entity types from data-model.md

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  createdAt: Date;
  updatedAt: Date;
}

export type UserRole = 'admin' | 'user';

// [Add other entities from data-model.md]
```

---

## Base Components

### Error Handling

**File:** `src/lib/errors.ts`

```typescript
// Custom error classes

export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public fields?: Record<string, string>) {
    super(message, 'VALIDATION_ERROR', 400);
    this.name = 'ValidationError';
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 'UNAUTHORIZED', 401);
    this.name = 'UnauthorizedError';
  }
}
```

---

### Logging

**File:** `src/lib/logger.ts`

```typescript
// Logging utility

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogContext {
  [key: string]: unknown;
}

class Logger {
  private log(level: LogLevel, message: string, context?: LogContext) {
    const entry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      ...context,
    };

    console[level](JSON.stringify(entry));
  }

  debug(message: string, context?: LogContext) {
    this.log('debug', message, context);
  }

  info(message: string, context?: LogContext) {
    this.log('info', message, context);
  }

  warn(message: string, context?: LogContext) {
    this.log('warn', message, context);
  }

  error(message: string, error?: Error, context?: LogContext) {
    this.log('error', message, {
      ...context,
      error: error ? { message: error.message, stack: error.stack } : undefined,
    });
  }
}

export const logger = new Logger();
```

---

### Database Client

**File:** `src/lib/db.ts`

```typescript
// Database client setup
// [Adjust based on stack.md database choice]

import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const db = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query'] : [],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = db;
}
```

---

## Utilities

### Common Helpers

**File:** `src/utils/index.ts`

```typescript
// Utility functions

/**
 * Sleep for specified milliseconds
 */
export const sleep = (ms: number) =>
  new Promise(resolve => setTimeout(resolve, ms));

/**
 * Generate a random ID
 */
export const generateId = () =>
  crypto.randomUUID();

/**
 * Safe JSON parse with fallback
 */
export const safeJsonParse = <T>(json: string, fallback: T): T => {
  try {
    return JSON.parse(json);
  } catch {
    return fallback;
  }
};

/**
 * Omit keys from object
 */
export const omit = <T extends object, K extends keyof T>(
  obj: T,
  keys: K[]
): Omit<T, K> => {
  const result = { ...obj };
  keys.forEach(key => delete result[key]);
  return result;
};

/**
 * Pick keys from object
 */
export const pick = <T extends object, K extends keyof T>(
  obj: T,
  keys: K[]
): Pick<T, K> => {
  const result = {} as Pick<T, K>;
  keys.forEach(key => {
    if (key in obj) result[key] = obj[key];
  });
  return result;
};
```

---

## API Structure

### Route Organization

**File:** `src/api/index.ts`

```typescript
// API route organization
// [Adjust based on framework]

import { Router } from 'express';
import { userRoutes } from './routes/users';
// import other routes

const router = Router();

router.use('/users', userRoutes);
// mount other routes

export { router as apiRouter };
```

### Route Template

**File:** `src/api/routes/[resource].ts`

```typescript
// Route template pattern

import { Router } from 'express';
import { z } from 'zod';

const router = Router();

// GET /resource
router.get('/', async (req, res, next) => {
  try {
    // Implementation
    res.json({ data: [] });
  } catch (error) {
    next(error);
  }
});

// GET /resource/:id
router.get('/:id', async (req, res, next) => {
  try {
    const { id } = req.params;
    // Implementation
    res.json({ data: {} });
  } catch (error) {
    next(error);
  }
});

// POST /resource
router.post('/', async (req, res, next) => {
  try {
    // Validate input
    // Create resource
    res.status(201).json({ data: {} });
  } catch (error) {
    next(error);
  }
});

export { router as resourceRoutes };
```

---

## Frontend Scaffolding (if applicable)

### Component Structure

**File:** `src/components/ui/Button.tsx`

```tsx
// Base component pattern

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  disabled
}: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
```

---

## Scaffolding Checklist

### Configuration

- [ ] TypeScript configured
- [ ] Linting configured
- [ ] Formatting configured
- [ ] Environment handling set up

### Base Code

- [ ] Error classes created
- [ ] Logger utility created
- [ ] Database client set up
- [ ] Common utilities created

### Structure

- [ ] Type definitions in place
- [ ] API route structure established
- [ ] Component patterns defined (if frontend)

### Verification

- [ ] Project compiles without errors
- [ ] Linting passes
- [ ] Base patterns work as expected

---

## Patterns Established

<!-- Document patterns for consistency -->

| Pattern | Location | Description |
|---------|----------|-------------|
| Error handling | `src/lib/errors.ts` | Custom error classes |
| Logging | `src/lib/logger.ts` | Structured JSON logging |
| API responses | `src/types/index.ts` | Consistent response shapes |
| [Pattern] | [Location] | [Description] |

---

## Related Documents

- [repo-init.md](repo-init.md) - Repository setup
- [architecture.md](../design/templates/architecture.md) - System structure
- [stack.md](../design/templates/stack.md) - Technology choices
