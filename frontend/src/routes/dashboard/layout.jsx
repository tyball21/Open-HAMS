import { Sidebar } from "@/components/sidebar";
import { Outlet } from "react-router-dom";

export function DashboardLayout() {
  return (
      <body className="bg-body mx-auto flex min-h-screen bg-blueish">
        <div className="fixed left-0 top-0 hidden h-full w-56 lg:block">
          <Sidebar />
        </div>
        <main className="flex flex-1 flex-col overflow-y-auto lg:ml-56">
          <div className="px-4 py-4 lg:px-8">
            <Outlet />
          </div>
        </main>
      </body>
  );
}
