import { ScrollList } from "@/components/scroll-list";

import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu, Plus } from "lucide-react";

import { EventsCalendar } from "@/components/events-calendar";
import { Sidebar } from "@/components/sidebar";
import { LiveFeed } from "@/components/live-feed";

export function DashboardPage() {
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
      <div className="my-10 grid grid-cols-1 gap-8 md:grid-cols-2 xl:grid-cols-4 xl:gap-24">
        <ScrollList title="Live Events" />
        <ScrollList title="Upcoming Events" />
        <ScrollList title="Checked Out" />
        <ScrollList title="Resting" />
      </div>
      <div className="mt-10 grid grid-cols-1 gap-8 2xl:grid-cols-2 2xl:gap-24">
        <EventsCalendar />
        <LiveFeed />
      </div>
      <div className="mt-10 grid grid-cols-1 lg:grid-cols-2"></div>
    </>
  );
}
