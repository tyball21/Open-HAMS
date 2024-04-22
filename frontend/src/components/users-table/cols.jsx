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
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "email",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Email" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("email")}</span>
        </div>
      );
    },
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "role",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Role" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("role")}</span>
        </div>
      );
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
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "actionDate",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Action Date" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("actionDate")}</span>
        </div>
      );
    },
  },
  {
    accessorKey: "deptName",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Department Name" />
    ),
    cell: ({ row }) => {
      return <p>{row.getValue("deptName")}</p>;
    },
    filterFn: (row, id, value) => {
      return row[id].toLowerCase().includes(value.toLowerCase());
    },
  },
  {
    accessorKey: "createdAt",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Account Created At" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("createdAt")}</span>
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
