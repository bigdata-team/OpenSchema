pnpm init
mkdir apps
echo "packages:\n  - 'apps/**/*'" > pnpm-workspace.yaml

pnpm create vite ./apps/remote
pnpm create vite ./apps/host

pnpm add -Dw @module-federation/vite
pnpm add -r react react-router
pnpm add -rD tailwindcss @tailwindcss/vite postcss autoprefixer

https://ui.shadcn.com/docs/installation/vite