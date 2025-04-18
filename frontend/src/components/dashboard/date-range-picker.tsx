import { format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";
import * as React from "react";
import { DateRange } from "react-day-picker";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/utils";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

interface DatePicketWithRangeProps
  extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
  date?: DateRange;
  setDate: (date: DateRange | undefined) => void;
  showSingleDayOption?: boolean;
}

export function DatePickerWithRange({
  className,
  date,
  setDate,
  showSingleDayOption = true, // Default to showing the option
}: DatePicketWithRangeProps) {
  const [isSingleDay, setIsSingleDay] = React.useState(false);
  
  // Handle changes to the single day checkbox
  const handleSingleDayChange = (checked: boolean) => {
    setIsSingleDay(checked);
    
    // If checked and we have a start date, make the end date match the start date
    if (checked && date?.from) {
      setDate({ from: date.from, to: date.from });
    }
  };
  
  // Handle calendar date selection with single day mode awareness
  const handleDateSelect = (newDate: DateRange | undefined) => {
    if (isSingleDay && newDate?.from) {
      // In single day mode, always set end date equal to start date
      setDate({ from: newDate.from, to: newDate.from });
    } else {
      // Normal date range selection
      setDate(newDate);
    }
  };

  return (
    <div className={cn("grid gap-2", className)}>
      <Popover>
        <PopoverTrigger asChild>
          <Button
            id="date"
            variant={"outline"}
            className={cn(
              "w-[300px] justify-start text-left font-normal",
              !date && "text-muted-foreground",
            )}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {date?.from ? (
              date.to && date.from !== date.to ? (
                <>
                  {format(date.from, "LLL dd, y")} -{" "}
                  {format(date.to, "LLL dd, y")}
                </>
              ) : (
                format(date.from, "LLL dd, y")
              )
            ) : (
              <span>Pick a date</span>
            )}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            initialFocus
            mode="range"
            defaultMonth={date?.from}
            selected={date}
            onSelect={handleDateSelect}
            numberOfMonths={2}
            disabled={isSingleDay ? date => false : undefined}
          />
          {showSingleDayOption && (
            <div className="border-t p-3 flex items-center space-x-2">
              <Checkbox 
                id="single-day" 
                checked={isSingleDay}
                onCheckedChange={handleSingleDayChange}
              />
              <Label htmlFor="single-day" className="text-sm font-normal cursor-pointer">
                One-day event
              </Label>
            </div>
          )}
        </PopoverContent>
      </Popover>
    </div>
  );
}
