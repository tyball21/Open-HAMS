import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DateRangePicker } from "../data-range-picker";
import { Button } from "../ui/button";
import { Label } from "../ui/label";

export function ReportsSettings() {
  return (
    <section className="mt-8 w-full rounded-md bg-white p-8 shadow-sm">
      <div className="mt-10 w-full max-w-[900px] rounded-lg border bg-white p-8 shadow-sm">
        <div className="flex w-full max-w-[400px] flex-col gap-8">
          <Select className="w-full">
            <SelectTrigger className="">
              <SelectValue placeholder="Select Export Category" />
            </SelectTrigger>
            <SelectContent>
              {["Events", "Users", "Animals"].map((group) => (
                <SelectItem key={group} value={group}>
                  {group}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <div className="flex flex-col gap-2">
            <Label>Select Date Range</Label>
            <DateRangePicker className="w-full" />
          </div>

          <Button className="w-full">Generate Report</Button>
        </div>
      </div>
    </section>
  );
}
