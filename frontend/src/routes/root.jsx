import { Sidebar } from "@/components/sidebar";
import { ThemeProvider } from "@/components/theme-provider";

export function RootLayout() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <body className="bg-body mx-auto flex h-screen bg-[#F0F8FF]">
        <Sidebar />
        Hello from Vite!
      </body>
    </ThemeProvider>
  );
}
