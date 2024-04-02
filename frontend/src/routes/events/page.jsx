import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu, Plus } from "lucide-react";

import { columns } from "@/components/events-table/cols";
import { DataTable } from "@/components/events-table/data-table";
import { Sidebar } from "@/components/sidebar";

function getDummyData() {
  return Array.from({ length: 100 }).map(() => ({
    image: "https://avartation-api.vercel.app/api",
    name: `Max`,
    description: `This is a description for Event`,
    eventDate: `2021-09-01`,
    location: "New York",
    assignedAnimals: 5,
    status: "Planned",
    lastEditedBy: "John Doe",
    date: "2021-09-01",
  }));
}

export function EventsPage() {
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
          Create New Event
        </Button>
      </header>
      <div className="mt-10 w-full rounded-lg bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-2xl font-semibold">All Events</h2>
        <DataTable data={data} columns={columns} />
      </div>
    </>
  );
}
