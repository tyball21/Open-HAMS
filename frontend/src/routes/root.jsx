import { ThemeProvider } from "@/components/theme-provider";

export function RootLayout() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <body className="container mx-auto flex h-screen flex-col items-center justify-center">
        Hello from Vite!
      </body>
    </ThemeProvider>
  );
}
