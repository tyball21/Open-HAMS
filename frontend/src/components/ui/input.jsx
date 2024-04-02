import { Search as SearchIcon } from "lucide-react";
import * as React from "react";

import { cn } from "@/lib/utils";

const Input = React.forwardRef(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      ref={ref}
      {...props}
    />
  );
});
Input.displayName = "Input";

export { Input };

const Search = React.forwardRef(({ className, ...props }, ref) => {
  return (
    <div
      className={cn(
        "flex h-10 items-center rounded-md border border-input bg-transparent pl-3 text-sm ring-offset-background focus-within:ring-1 focus-within:ring-ring focus-within:ring-offset-2",
        className,
      )}
    >
      <SearchIcon className="h-[16px] w-[16px]" />
      <input
        {...props}
        type="search"
        ref={ref}
        className="w-full bg-background p-2 placeholder:text-muted-foreground focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50"
      />
    </div>
  );
});

Search.displayName = "Search";

export { Search };
