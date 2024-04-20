import { Input } from "@/components/ui/input";

export function RolesToolbar({ table }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <div className=" flex flex-1 items-center space-x-2">
        <Input
          placeholder="Search users..."
          value={table.getColumn("name")?.getFilterValue() ?? ""}
          onChange={(event) =>
            table.getColumn("name")?.setFilterValue(event.target.value)
          }
          className="max-w-[400px]"
        />
      </div>
    </div>
  );
}
