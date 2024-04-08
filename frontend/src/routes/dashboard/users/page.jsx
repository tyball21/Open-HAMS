import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu, Plus } from "lucide-react";

import { columns } from "@/components/users-table/cols";
import { DataTable } from "@/components/users-table/data-table";
import { Sidebar } from "@/components/sidebar";

function getDummyData() {
  return Array.from({ length: 5 }).map((_, index) => ({
    image: "https://avartation-api.vercel.app/api",
    name: `User ${index + 1}`,
    email: `user${index + 1}@HAMS.com`,
    role: Math.random() > 0.5 ? "Admin" : "User",
    lastAction: "New Event",
    actionDate: "2021-09-01",
    deptName: "Ambassador",
    createdAt: "2021-09-01",
  }));
}

export function AnimalsPage() {
  const data = getDummyData();

  return (
    <>
      <header className="flex items-center justify-between px-2 lg:px-4">
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="lg:hidden">
              <Menu />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="m-0 w-56 p-0">
            <Sidebar />
          </SheetContent>
        </Sheet>
        <Button className="ml-auto">
          <Plus className="mr-2 size-4" />
          Create New User
        </Button>
      </header>
      <div className="mt-10 w-full rounded-lg bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-2xl font-semibold">All Users</h2>
        <DataTable data={data} columns={columns} />
      </div>
    </>
  );
}
