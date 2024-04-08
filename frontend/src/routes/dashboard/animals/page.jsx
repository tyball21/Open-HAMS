import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu, Plus } from "lucide-react";

import { columns } from "@/components/animals-table/cols";
import { DataTable } from "@/components/animals-table/data-table";
import { Sidebar } from "@/components/sidebar";

function getDummyData() {
  return Array.from({ length: 5 }).map((_, index) => ({
    image: "https://avartation-api.vercel.app/api",
    name: `Cat ${index + 1}`,
    breed: "Domestic Short Hair",
    age: 4,
    species: "Cat",
    status: "Checked In",
    lastAction: "Checked In",
    lastCompletedBy: "John Doe",
    date: "2021-09-01",
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
          Add New Animal
        </Button>
      </header>
      <div className="mt-10 w-full rounded-lg bg-white p-8 shadow-sm border">
        <h2 className="mb-4 text-2xl font-semibold">All Animals</h2>
        <DataTable data={data} columns={columns} />
      </div>
    </>
  );
}
