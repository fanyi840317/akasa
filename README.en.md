# Akasa - Mysterious Event Recording Platform

Akasa is a modern platform for recording and sharing mysterious events, allowing users to document their extraordinary experiences in an elegant way.

## Project Structure

```
akasa/
├── web.app/                          # Frontend Application
│   ├── src/                          # Source Code
│   │   ├── lib/                      # Shared Libraries and Components
│   │   │   ├── components/          # UI Components
│   │   │   │   ├── ui/             # Base UI Components
│   │   │   │   ├── events/         # Event-related Components
│   │   │   │   ├── map/            # Map-related Components
│   │   │   │   └── editor/         # Editor-related Components
│   │   │   ├── stores/             # State Management
│   │   │   │   ├── auth.store.ts   # Authentication State
│   │   │   │   ├── event.store.ts  # Event State
│   │   │   │   └── ui.store.ts     # UI State
│   │   │   ├── types/              # TypeScript Type Definitions
│   │   │   │   ├── event.types.ts  # Event-related Types
│   │   │   │   ├── user.types.ts   # User-related Types
│   │   │   │   └── map.types.ts    # Map-related Types
│   │   │   ├── utils/              # Utility Functions
│   │   │   │   ├── date.ts         # Date Handling
│   │   │   │   ├── format.ts       # Formatting Utilities
│   │   │   │   └── validation.ts   # Validation Utilities
│   │   │   └── i18n/               # Internationalization
│   │   │       ├── locales/        # Translation Files
│   │   │       └── index.ts        # i18n Configuration
│   │   ├── routes/                 # Page Routes
│   │   │   ├── (auth)/            # Authentication Pages
│   │   │   ├── (main)/            # Main Pages
│   │   │   └── +layout.svelte     # Root Layout
│   │   ├── app.css                 # Global Styles
│   │   └── app.d.ts                # Global Type Declarations
│   ├── static/                     # Static Assets
│   │   ├── images/                 # Image Resources
│   │   ├── fonts/                  # Font Files
│   │   └── icons/                  # Icon Resources
│   ├── tests/                      # Test Files
│   │   ├── unit/                   # Unit Tests
│   │   └── integration/            # Integration Tests
│   ├── tailwind.config.ts          # Tailwind Configuration
│   ├── svelte.config.js            # Svelte Configuration
│   ├── vite.config.ts              # Vite Configuration
│   └── package.json                # Project Dependencies
├── db/                             # Database Related
│   ├── migrations/                 # Database Migrations
│   ├── seeds/                      # Database Seeds
│   └── schema/                     # Database Schema
└── package.json                    # Root Project Dependencies
```

### Directory Structure

#### web.app/
Main frontend application directory containing all frontend-related code and configurations.

- **src/**: Source code directory
  - **lib/**: Shared libraries and components
    - **components/**: UI components directory
      - **ui/**: Base UI components (buttons, inputs, etc.)
      - **events/**: Event-related components (event cards, forms, etc.)
      - **map/**: Map-related components (map selector, location markers, etc.)
      - **editor/**: Editor-related components (rich text editor, etc.)
    - **stores/**: State management directory
      - **auth.store.ts**: User authentication state management
      - **event.store.ts**: Event data state management
      - **ui.store.ts**: UI state management
    - **types/**: TypeScript type definitions directory
      - **event.types.ts**: Event-related type definitions
      - **user.types.ts**: User-related type definitions
      - **map.types.ts**: Map-related type definitions
    - **utils/**: Utility functions directory
      - **date.ts**: Date handling utilities
      - **format.ts**: Data formatting utilities
      - **validation.ts**: Data validation utilities
    - **i18n/**: Internationalization directory
      - **locales/**: Multi-language translation files
      - **index.ts**: i18n configuration
  - **routes/**: Page routes directory
    - **(auth)/**: Authentication-related pages
    - **(main)/**: Main feature pages
    - **+layout.svelte**: Root layout component
  - **app.css**: Global styles file
  - **app.d.ts**: Global type declarations file

- **static/**: Static assets directory
  - **images/**: Image resources
  - **fonts/**: Font files
  - **icons/**: Icon resources

- **tests/**: Test files directory
  - **unit/**: Unit tests
  - **integration/**: Integration tests

#### db/
Database-related directory containing database migrations, seed data, and schema definitions.

- **migrations/**: Database migration files
- **seeds/**: Database seed data
- **schema/**: Database schema definitions

## Tech Stack

### Core Framework
- **Frontend Framework**: SvelteKit 2.0
- **Styling Framework**: Tailwind CSS 3.4
- **UI Components**: shadcn-svelte
- **Editor**: Affine Editor (based on BlockSuite)
- **State Management**: Svelte Stores
- **Type System**: TypeScript 5.0
- **Internationalization**: svelte-i18n 4.0

### Map Related
- **Map Engine**: Cesium.js
- **Map Service**: Mapbox GL
- **Map Components**: Leaflet

### Development Tools
- **Build Tool**: Vite
- **Package Manager**: pnpm
- **Code Checking**: svelte-check
- **Animation Library**: tailwindcss-animate
- **UI Component Libraries**: bits-ui, vaul-svelte
- **Icon Library**: Lucide Icons

### Backend Services
- **BaaS**: Appwrite 14.0
- **Analytics**: Vercel Analytics

## Development Guidelines

### Code Standards

1. **File Organization**
   - Component files in `src/lib/components`
   - Page files in `src/routes`
   - Type definitions in `src/lib/types`
   - Store files in `src/lib/stores`

2. **Naming Conventions**
   - File Naming:
     - Component files: `re-component-name.svelte` (e.g., `re-event-card.svelte`)
     - Utility files: `re-utils-name.ts` (e.g., `re-format-date.ts`)
     - Type files: `re-types-name.ts` (e.g., `re-event-types.ts`)
     - Store files: `re-store-name.ts` (e.g., `re-user-store.ts`)
     - Test files: `re-test-name.test.ts` (e.g., `re-event-card.test.ts`)
     - Style files: `re-style-name.css` (e.g., `re-event-card.css`)
     - Layout files: `+layout.svelte` (SvelteKit convention)
     - Page files: `+page.svelte` (SvelteKit convention)
     - Loading files: `+loading.svelte` (SvelteKit convention)
     - Error files: `+error.svelte` (SvelteKit convention)

   - Variable Naming:
     - Component variables: `PascalCase` (e.g., `EventCard`, `UserProfile`)
     - Regular variables: `PascalCase` (e.g., `UserName`, `EventDate`)
     - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_EVENTS`, `API_ENDPOINT`)
     - Types and interfaces: `PascalCase` (e.g., `User`, `EventData`)
     - Enums: `PascalCase` (e.g., `EventStatus`, `UserRole`)
     - Boolean variables: Use `Is`, `Has`, `Should` prefix (e.g., `IsLoading`, `HasError`)
     - Event handlers: Use `Handle` prefix (e.g., `HandleClick`, `HandleSubmit`)
     - Async functions: Use `Fetch`, `Load`, `Save` verbs (e.g., `FetchUserData`, `SaveEvent`)
     - Store variables: Use `Store` suffix (e.g., `UserStore`, `EventStore`)
     - Derived state: Use `$` prefix (e.g., `$User`, `$Event`)

   - Directory Naming:
     - Component directories: `PascalCase` (e.g., `EventCard/`)
     - Feature directories: `PascalCase` (e.g., `UserProfile/`)
     - Utility directories: `PascalCase` (e.g., `Utils/`)
     - Type directories: `Types/`
     - Test directories: `__Tests__/`
     - Style directories: `Styles/`
     - Asset directories: `Assets/`

   - Import Naming:
     ```typescript
     // Component imports
     import EventCard from '$lib/components/events/re-event-card.svelte';
     
     // Type imports
     import type { Event, User } from '$lib/types/re-event-types';
     
     // Store imports
     import { UserStore } from '$lib/stores/re-user-store';
     
     // Utility function imports
     import { FormatDate } from '$lib/utils/re-format-date';
     ```

   - CSS Class Naming:
     - Use Tailwind class names
     - Custom class names use `PascalCase`
     - Component-specific classes use `re-component-name-class` format
     - State classes use `Is` prefix (e.g., `IsActive`, `IsDisabled`)
     - Theme classes use `Theme` prefix (e.g., `ThemeDark`, `ThemeLight`)

### Component Development Standards

1. **Component Design Principles**
   - Single Responsibility
   - Reusability
   - Testability
   - Maintainability

2. **Component Documentation**
   ```svelte
   <!-- re-event-card.svelte -->
   <script lang="ts">
     /**
      * @component EventCard
      * @description Component for displaying event information
      * 
      * @prop {string} Title - Event title
      * @prop {string} Description - Event description
      * @prop {Date} Date - Event date
      * @prop {string} Location - Event location
      * 
      * @event {CustomEvent} Click - Click event
      */
     
     interface Props {
       Title: string;
       Description?: string;
       Date: Date;
       Location: string;
     }
     
     let { Title, Description, Date, Location }: Props = $props();
   </script>
   ```

3. **Component Testing**
   ```typescript
   // re-event-card.test.ts
   import { render, screen } from '@testing-library/svelte';
   import EventCard from './re-event-card.svelte';
   
   describe('EventCard', () => {
     it('renders event title', () => {
       render(EventCard, {
         props: {
           Title: 'Test Event',
           Date: new Date(),
           Location: 'Test Location'
         }
       });
       
       expect(screen.getByText('Test Event')).toBeInTheDocument();
     });
   });
   ```

### Performance Optimization Standards

1. **Component Optimization**
   - Use `$:reactive` declarations
   - Avoid unnecessary computations
   - Use `svelte:component` for dynamic loading
   - Use `bind:this` appropriately

2. **State Management Optimization**
   - Avoid excessive global state
   - Use derived state
   - Use subscriptions appropriately

3. **Resource Optimization**
   - Lazy load images
   - Lazy load components
   - Use caching appropriately

## Development Process

1. **Environment Setup**
   ```bash
   # Install dependencies
   pnpm install

   # Start development server
   pnpm dev

   # Build production version
   pnpm build

   # Run code checks
   pnpm check
   ```

2. **Development Workflow**
   ```bash
   # 1. Create feature branch
   git checkout -b feature/new-feature

   # 2. Develop feature
   # 3. Commit changes
   git add .
   git commit -m "feat: add new feature"

   # 4. Push to remote
   git push origin feature/new-feature

   # 5. Create Pull Request
   ```

3. **Code Review**
   - Follow code standards
   - Ensure tests pass
   - Check performance impact
   - Update documentation

## Deployment Guide

1. **Environment Requirements**
   - Node.js 18+
   - pnpm 8+
   - Appwrite 14.0+

2. **Deployment Steps**
   ```bash
   # 1. Install dependencies
   pnpm install

   # 2. Build project
   pnpm build

   # 3. Preview build
   pnpm preview
   ```

3. **Environment Variables**
   - Create `.env` file
   - Configure required variables:
     ```
     PUBLIC_APPWRITE_ENDPOINT=
     PUBLIC_APPWRITE_PROJECT_ID=
     PUBLIC_MAPBOX_TOKEN=
     ```

## Contributing Guidelines

1. Fork the project
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License
