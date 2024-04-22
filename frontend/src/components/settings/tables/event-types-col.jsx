import { Avatar, AvatarImage } from "@/components/ui/avatar";
import { DataTableColumnHeader } from "./col-headers";

import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export const eventTypesColumns = [
  {
    accessorKey: "image",
    header: ({ column }) => <DataTableColumnHeader column={column} title="" />,
    cell: ({ row }) => (
      <Avatar className="m-2">
        <AvatarImage src={row.getValue("image")} alt={row.getValue("name")} />
      </Avatar>
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "eventTypeName",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Event Type Name" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("eventTypeName")}</span>
        </div>
      );
    },
  },
  {
    accessorKey: "group",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Group" />
    ),
    cell: ({ row }) => {
      const defaultGroup = row.getValue("group");
      return (
        <Select>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Group" defaultValue={defaultGroup} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="group-1">Group 1</SelectItem>
            <SelectItem value="group-2">Group 2</SelectItem>
            <SelectItem value="group-3">Group 3</SelectItem>
          </SelectContent>
        </Select>
      );
    },
  },
  {
    id: "actions",
    cell: () => (
      <Badge variant="secondary" className="font-thin">
        edit
      </Badge>
    ),
  },
];
