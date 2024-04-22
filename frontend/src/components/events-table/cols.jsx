import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Badge } from "../ui/badge";
import { DataTableColumnHeader } from "./col-headers";

export const columns = [
  {
    accessorKey: "image",
    header: ({ column }) => <DataTableColumnHeader column={column} title="" />,
    cell: ({ row }) => (
      <Avatar className="m-2">
        <AvatarImage src={row.getValue("image")} alt={row.getValue("name")} />
        <AvatarFallback>{row.getValue("name")[0]}</AvatarFallback>
      </Avatar>
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "name",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Name" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("name")}</span>
        </div>
      );
    },
  },
  {
    accessorKey: "description",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Description" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("description")}</span>
        </div>
      );
    },
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "eventDate",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Event Date" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("eventDate")}</span>
        </div>
      );
    },
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "location",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Location" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("location")}</span>
        </div>
      );
    },
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "assignedAnimals",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Assigned Animals" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("assignedAnimals")}</span>
        </div>
      );
    },
  },
  {
    accessorKey: "status",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Status" />
    ),
    cell: ({ row }) => {
      return <p>{row.getValue("status")}</p>;
    },
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "lastEditedBy",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Last Edited By" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("lastEditedBy")}</span>
        </div>
      );
    },
  },

  {
    accessorKey: "date",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Date" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("date")}</span>
        </div>
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
