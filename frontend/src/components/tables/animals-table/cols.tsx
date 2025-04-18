import { useUser } from "@/api/queries";
import { AnimalModel } from "@/components/models/animal-model";
import { Button } from "@/components/ui/button";
import { hasPermission } from "@/utils";
import { Animal } from "@/utils/types";
import { ColumnDef } from "@tanstack/react-table";
import { Avatar, AvatarFallback, AvatarImage } from "../../ui/avatar";
import { DataTableColumnHeader } from "../table-commons/col-headers";

export const animalTableColumns: ColumnDef<Animal>[] = [
  {
    accessorKey: "image",
    header: ({ column }) => <DataTableColumnHeader column={column} title="" />,
    cell: ({ row }) => {
      const imageField = (row.original as any)["image_filename"] || (row.original as any)["image"];
      const imageUrl = imageField ? `/static/animal_images/${imageField}` : undefined;
      return (
        <Avatar className="m-2">
          <AvatarImage src={imageUrl} alt={row.original.name} />
          <AvatarFallback>{row.original.name[0]}</AvatarFallback>
        </Avatar>
      );
    },
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "id",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="System ID" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("id")}</span>
        </div>
      );
    },
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
  },
  {
    accessorKey: "max_daily_checkout_hours",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Max Daily Checkout Hours" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("max_daily_checkout_hours")}</span>
        </div>
      );
    },
  },
  {
    accessorKey: "max_daily_checkouts",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Max Daily Checkouts" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("max_daily_checkouts")}</span>
        </div>
      );
    },
  },
  {
    accessorKey: "rest_time",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Rest Time" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("rest_time")}</span>
        </div>
      );
    },
  },
  {
    accessorKey: "tier",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Tier" />
    ),
    cell: ({ row }) => {
      return <p>{row.getValue("tier")}</p>;
    },
  },
  {
    id: "createdAt",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Date" />
    ),
    cell: ({ row }) => {
      return (
        <div className="flex items-center">
          <span>{row.getValue("createdAt")}</span>
        </div>
      );
    },
    accessorFn: (row) => new Date(row.created_at).toLocaleDateString(),
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const user = useUser();

      if (user.isLoading) {
        return null;
      }

      if (!hasPermission(user?.data!, "update_animals")) {
        return null;
      }

      return (
        <AnimalModel mode="edit" animalId={row.getValue("id")}>
          <Button
            variant="secondary"
            className="rounded-full font-light"
            size="xs"
          >
            edit
          </Button>
        </AnimalModel>
      );
    },
  },
];
