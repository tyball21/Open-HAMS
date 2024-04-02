import { Sidebar } from "@/components/sidebar";
import { ThemeProvider } from "@/components/theme-provider";
import { Outlet } from "react-router-dom";

export function RootLayout() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
      <body className="bg-body mx-auto flex h-screen bg-blueish">
        <div className="bg-myRed hidden w-56 lg:block">
          <Sidebar />
        </div>
        <main className="flex-1 px-4 py-4 lg:px-8">
          <Outlet />
        </main>
      </body>
    </ThemeProvider>
  );
}
