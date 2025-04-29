import { Button } from "@/components/ui/button";

import { ScrollArea } from "@/components/ui/scroll-area";
import { ArrowRight } from "lucide-react";
import { LoadingDots } from "../icons";

type Props = {
  title: React.ReactNode;
  isLoading?: boolean;
  children: React.ReactNode;
};

export function ScrollList({ title, children, isLoading = false }: Props) {
  return (
    <div className="w-full overflow-clip rounded-xl bg-white">
      <h2 className="flex items-center px-4 py-3 text-[18px] font-bold text-foreground">
        {title}
        <Button size="icon" className="ml-auto size-6 rounded-2xl">
          <ArrowRight className="size-4 text-white" />
        </Button>
      </h2>
      {isLoading ? (
        <div className="flex h-[162px] items-center justify-center">
          <LoadingDots />
        </div>
      ) : (
        <ScrollArea className="flex h-[162px] flex-col gap-2 p-2">
          {children}
        </ScrollArea>
      )}
    </div>
  );
}
