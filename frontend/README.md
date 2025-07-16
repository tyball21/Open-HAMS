# Frontend for HAMS

## Technologies Used

- Typescript
- React
- Tailwind
- Shadcn / Radix UI
- Zod (for Data Validation)
- React Hook Forms

## Instructions

1. Install Dependencies

```shell
   pnpm i
```

2. Run dev server

```shell
   pnpm run dev
```

> Make sure to add a .env file with same configuration as in .env.example

## Production Deployment

### Build for Production

```shell
pnpm run build
```

This creates a `dist/` directory with optimized static files ready for production.

### Local Production Preview

```shell
pnpm run preview
```

This serves the built files locally to test the production build.

### Deployment Options

#### Option 1: Static Hosting Platforms
Deploy the `dist/` folder to platforms like:
- **Vercel**: Auto-detects Vite projects
- **Netlify**: Auto-detects Vite projects  
- **GitHub Pages**: Serve from `dist/` folder

#### Option 2: Render Web Service
When setting up a new Web Service on Render:
- **Build Command**: `pnpm install && pnpm run build`
- **Start Command**: `npx serve -s dist`
- **Publish Directory**: `dist`

#### Option 3: Self-Hosted
After building, serve the `dist/` folder with any static file server:

```shell
# Using serve (recommended)
npx serve -s dist

# Using Python's built-in server
cd dist && python -m http.server 3000

# Using Node.js http-server
npx http-server dist -p 3000
```

### Environment Variables

Make sure to configure your production environment variables in your hosting platform's dashboard, matching the structure from `.env.example`.

## Contributing

Thank you for your interest in contributing to our project! We welcome contributions from everyone and are grateful for every pull request.

### Prerequisites

- Familarity with React and Typescript
- Familiarity with Git

### Coding Standards

Please follow the coding style and conventions established in the project. Use Prettier.

### Submitting Changes

1. Create a new branch for your changes.
2. Make your changes and commit them with clear, concise commit messages.
3. Push your branch and submit a pull request to the main repository.
4. Await code review and address any feedback.

### Code Review Process

All submissions require review. We aim to review and respond to your pull request within 3 days.

### Community and Communication

Join our community on [Discord](https://discord.gg/CVxRvMzqWQ) for discussions and support.
