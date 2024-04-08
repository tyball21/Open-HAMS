import { ThemeProvider } from "@/components/theme-provider";
import { Outlet } from "react-router-dom";

export function RootLayout() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
      <Outlet />
    </ThemeProvider>
  );
}
