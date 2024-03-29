import { Sidebar } from "@/components/sidebar";
import { ThemeProvider } from "@/components/theme-provider";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { ArrowRight, Menu, Plus } from "lucide-react";

export function RootLayout() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <body className="bg-body bg-blueish mx-auto flex h-screen">
        <div className="bg-myRed hidden w-56 lg:block">
          <Sidebar />
        </div>
        <main className="flex-1 px-4 py-4 lg:px-8">
          <header className="flex items-center justify-between px-2 lg:px-4">
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="outline" size="icon" className="lg:hidden">
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
          <div className="mt-10 grid grid-cols-1 gap-24 md:grid-cols-2 lg:grid-cols-4">
            <ScrollList title="Live Events" />
            <ScrollList title="Upcoming Events" />
            <ScrollList title="Checked Out" />
            <ScrollList title="Resting" />
          </div>
        </main>
      </body>
    </ThemeProvider>
  );
}

function ScrollList({ title = "Live Events" }) {
  return (
    <div className="w-full overflow-clip rounded-xl bg-white">
      <h2 className="flex items-center px-8 py-3 text-[18px] font-bold text-foreground">
        {title}
        <Button size="icon" className="ml-auto size-6 rounded-2xl">
          <ArrowRight className="size-4 text-white" />
        </Button>
      </h2>
      <Separator />
      <ScrollArea className="h-[121px]">
        <ul className="h-6">
          {Array.from({ length: 20 }).map((_, i) => (
            <li
              key={i}
              className="flex items-center border-b px-8 py-2 text-[#49535E]"
            >
              <p>Item {i + 1}</p>
              <Badge
                variant="secondary"
                className="ml-auto font-light text-[#1F2937]"
              >
                edit
              </Badge>
            </li>
          ))}
        </ul>
      </ScrollArea>
    </div>
  );
}
