import { ScrollList } from "@/components/dashboard/scroll-list";

import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu } from "lucide-react";

import {
  useCheckedoutAnimals,
  useRestingAnimals,
  useUpcomingLiveEvents,
  useUser,
} from "@/api/queries";
import Calendar from "@/components/big-calendar";
import { ListItem } from "@/components/dashboard/list-item";
import { LiveFeed } from "@/components/dashboard/live-feed";
import { EventHoverCard } from "@/components/events/event-hover-card";
import { HealthLogBox } from "@/components/events/health-log-box";
import { NewEventModel } from "@/components/events/new-event-model";
import { Sidebar } from "@/components/sidebar";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { hasPermission, timeTill } from "@/utils";
import { EventsCalendar } from "@/components/dashboard/events-calendar";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

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
        <NewEventModelButton />
      </header>
      <div className="my-10 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4 2xl:gap-12">
        <UpcomingLiveEvents />
        <CheckedOutAnimals />
        <RestingAnimals />
      </div>
      <div className="mt-10 grid h-[480px] grid-cols-1 gap-4 2xl:grid-cols-5 2xl:gap-8">
        <EventsCalendar />
        {/* <div className="col-span-3 grid gap-1 rounded-lg bg-white px-2 py-2 shadow-sm md:grid-cols-2">
          <Calendar />
        </div> */}
        <LiveFeed />
      </div>
    </>
  );
}

export function NewEventModelButton() {
  const { data: user, isLoading } = useUser();

  if (isLoading) {
    return null;
  }

  if (!hasPermission(user!, "create_events")) {
    return null;
  }

  return (
    <div className="ml-auto">
      <NewEventModel />
    </div>
  );
}

function UpcomingLiveEvents() {
  const { data: upcomingLiveEvents, isLoading } = useUpcomingLiveEvents();

  return (
    <>
      <ScrollList
        title={
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger className="cursor-default">
                Live Events
              </TooltipTrigger>
              <TooltipContent>
                <p>Events currently in progress</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        }
        isLoading={isLoading}
      >
        {upcomingLiveEvents?.live.map((event_details) => (
          <ListItem
            key={event_details.event.id}
            title={event_details.event.name}
            description={`Ends in ${timeTill(event_details.event.end_at)}`}
          >
            <EventHoverCard data={event_details} />
          </ListItem>
        ))}
        {upcomingLiveEvents?.live?.length === 0 && (
          <div className="flex h-[162px] items-center justify-center text-xs text-muted-foreground">
            No live events
          </div>
        )}
      </ScrollList>
      <ScrollList title="Upcoming Events" isLoading={isLoading}>
        {upcomingLiveEvents?.upcoming.map((event_details) => (
          <ListItem
            key={event_details.event.id}
            title={event_details.event.name}
            description={`Starts in ${timeTill(event_details.event.start_at)}`}
          >
            <EventHoverCard data={event_details} />
          </ListItem>
        ))}
        {upcomingLiveEvents?.upcoming?.length === 0 && (
          <div className="flex h-[162px] items-center justify-center text-xs text-muted-foreground">
            No upcoming events
          </div>
        )}
      </ScrollList>
    </>
  );
}

function CheckedOutAnimals() {
  const { data: checkedOutAnimals, isLoading } = useCheckedoutAnimals();
  return (
    <ScrollList title="Checked Out" isLoading={isLoading}>
      {checkedOutAnimals?.map((animal_details) => (
        <ListItem
          key={animal_details.animal.id}
          title={animal_details.animal.name}
          description={`Ends in ${timeTill(animal_details.current_event.event.end_at)}`}
        >
          <EventHoverCard
            data={animal_details.current_event}
            title={animal_details.current_event.event.name}
          />
        </ListItem>
      ))}
      {checkedOutAnimals?.length === 0 && (
        <div className="flex h-[162px] items-center justify-center text-xs text-muted-foreground">
          No checkedout animals
        </div>
      )}
    </ScrollList>
  );
}

function RestingAnimals() {
  const { data: restingAnimals, isLoading } = useRestingAnimals();
  return (
    <ScrollList title="Resting" isLoading={isLoading}>
      {restingAnimals?.map((animal_details) => (
        <ListItem
          key={animal_details.animal_status.animal.id}
          title={animal_details.animal_status.animal.name}
          description={animal_details.animal_status.status_description}
        >
          <Card className="w-full rounded-md border-b bg-model px-3 py-2 shadow-lg">
            <div className="flex items-center justify-end">
              <Badge variant="secondary">Unavailable</Badge>
            </div>
            <div className="grid gap-2">
              <div className="flex items-center gap-2 text-xs">
                <span className="text-xs text-muted-foreground">
                  Weekly Event Activity:{" "}
                </span>
                {animal_details.weekly_event_activity_hours.toFixed(1)} hours
              </div>
              <div className="flex items-center gap-2 text-xs">
                <span className="text-xs text-muted-foreground">
                  Daily Event Count:{" "}
                </span>
                {animal_details.daily_checkout_count} /{" "}
                {animal_details.animal_status.animal.max_daily_checkouts}
              </div>
            </div>
            <HealthLogBox
              animalId={animal_details.animal_status.animal.id.toString()}
              healthLogs={animal_details.health_logs}
              compact
            />
          </Card>
        </ListItem>
      ))}
      {restingAnimals?.length === 0 && (
        <div className="flex h-[162px] items-center justify-center text-xs text-muted-foreground">
          No resting animals
        </div>
      )}
    </ScrollList>
  );
}
