import { useState } from "react";

import { Calendar } from "./ui/calendar";
import { Button } from "./ui/button";

import { Heart, Pencil } from "lucide-react";

export function EventsCalendar() {
  const [date, setDate] = useState(new Date());
  return (
    <div className="grid min-h-[450px] gap-8 rounded-lg bg-white px-8 py-10 shadow-sm border md:grid-cols-2">
      <Calendar
        mode="single"
        selected={date}
        onSelect={setDate}
        className="mx-auto items-center justify-center"
      />
      <div className="flex h-full min-h-[350px] w-full flex-col bg-[#E6EEF5] p-4">
        <h2 className="text-lg font-bold text-foreground">Event Name</h2>
        <p className="mb-4 mt-2">Event Description - Yoga in the Park</p>
        <p>{date.toDateString()}</p>
        <p>9:00 AM - 10:00 AM</p>
        <Button className="mt-auto w-full">
          <Heart className="mr-2 size-4" />
          Follow Event
        </Button>
        <Button
          className="mt-2 w-full border-primary bg-transparent text-primary"
          variant="outline"
        >
          <Pencil className="mr-2 size-4" />
          Edit
        </Button>
      </div>
    </div>
  );
}
