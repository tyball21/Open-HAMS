import { Dog } from "lucide-react";
import { ScrollArea } from "./ui/scroll-area";

export function LiveFeed() {
  var liveFeed = [
    {
      event: "Checked In",
      name: "Lilly Lizard",
      by: "John Doe",
    },
    {
      event: "Checked Out",
      name: "Lilly Lizard",
      by: "John Doe",
    },
  ];

  return (
    <ScrollArea className="h-[450px] rounded-lg border bg-white p-4 shadow-sm lg:p-8">
      <h2 className="text-lg font-bold text-foreground">Activity Feed</h2>
      <div className="mb-6 mt-4 lg:max-w-[450px] space-y-4">
        <h2 className="text-lg text-foreground">Today</h2>
        {liveFeed.map((feed, index) => (
          <ActivityItem key={index} feed={feed} />
        ))}
        <h2 className="text-lg text-foreground">Last Week</h2>
        {liveFeed.map((feed, index) => (
          <ActivityItem key={index} feed={feed} />
        ))}
        <h2 className="text-lg text-foreground">Last Month</h2>
        {liveFeed.map((feed, index) => (
          <ActivityItem key={index} feed={feed} />
        ))}
      </div>
    </ScrollArea>
  );
}

function ActivityItem({ feed }) {
  return (
    <div className="flex items-center gap-4 rounded-sm border p-2 px-4">
      <div className="flex items-center justify-center rounded-full bg-[#E6EEF5] p-4">
        <Dog className="size-8" />
      </div>
      <div className="flex w-full flex-col justify-between">
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-semibold">{feed.event}:</h3>
          <p className="">Lilly Lizard</p>
        </div>
        <div className="flex w-full items-center justify-between gap-2 text-sm">
          <p>by John Doe</p>
          <p className="">7:00 PM</p>
        </div>
      </div>
    </div>
  );
}
