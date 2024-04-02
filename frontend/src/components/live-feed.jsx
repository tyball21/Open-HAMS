import { ScrollArea } from "./ui/scroll-area";

export function LiveFeed() {
  var liveFeed = [
    {
      event: "Checked In",
      description: "Doggo has been checked in",
    },
    {
      event: "Checked Out",
      description: "Doggo has been checked out",
    },
    {
      event: "Checked In",
      description: "Max Verstappen won the Japanese Grand Prix",
    },
    {
      event: "Checked Out",
      description: "Doggo has been checked out",
    },
    {
      event: "Checked In",
      description: "Doggo has been checked in",
    },
    {
      event: "Checked Out",
      description: "Doggo has been checked out",
    },
  ];

  liveFeed = [...liveFeed, ...liveFeed, ...liveFeed, ...liveFeed, ...liveFeed];

  return (
    <ScrollArea className="h-[450px] rounded-lg bg-white p-4 shadow-sm lg:p-8">
      <h2 className="text-lg font-bold text-foreground">Live Feed</h2>
      <div className="mt-4 space-y-4">
        {liveFeed.map((feed, index) => (
          <Description
            key={index}
            title={feed.event}
            description={feed.description}
          />
        ))}
      </div>
    </ScrollArea>
  );
}

function Description({ title, description }) {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center text-[14px]">
        <h3 className="mr-3 font-bold">{title}:</h3>
        <p className="">{description}</p>
      </div>
    </div>
  );
}
