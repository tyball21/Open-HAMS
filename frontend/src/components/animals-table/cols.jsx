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
    accessorKey: "species",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Species" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("species")}</span>
        </div>
      );
    },
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "species",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Species" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("species")}</span>
        </div>
      );
    },
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "breed",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Breed" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("breed")}</span>
        </div>
      );
    },
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "age",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Age" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("age")}</span>
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
    accessorKey: "lastAction",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Last Action" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("lastAction")}</span>
        </div>
      );
    },
  },
  {
    accessorKey: "lastCompletedBy",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Last Completed By" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("lastCompletedBy")}</span>
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
