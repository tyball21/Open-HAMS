import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { ArrowRight } from "lucide-react";

export function ScrollList({ title = "Live Events" }) {
  return (
    <div className="w-full overflow-clip rounded-xl bg-white">
      <h2 className="flex items-center px-8 py-3 text-[18px] font-bold text-foreground">
        {title}
        <Button size="icon" className="ml-auto size-6 rounded-2xl">
          <ArrowRight className="size-4 text-white" />
        </Button>
      </h2>
      <Separator />
      <ScrollArea className="h-[162px]">
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
