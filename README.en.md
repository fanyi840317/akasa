# akasa

## Project Overview
A modern web application built with SvelteKit and Appwrite backend, providing efficient data management capabilities.

## Tech Stack
- **Frontend**: SvelteKit + Tailwind CSS
- **Backend**: Appwrite BaaS
- **Database**: Appwrite Database with JSON schema

## Quick Start
```bash
# Install dependencies
pnpm install

# Initialize database (requires Appwrite endpoint & API key)
node db/setup_database.js

# Start dev server
cd web.app && pnpm run dev
```

## Project Structure
`web.app/` contains:
- `src/routes/` - Page components
- `src/lib/` - Shared utilities
- `static/` - CSS/font assets

## Contribution Guidelines
1. Fork repository
2. Create feature branch
3. Submit PR with description
