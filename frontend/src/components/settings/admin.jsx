import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { DataTable } from "./tables/data-table";
import { eventTypesColumns } from "./tables/event-types-col";
import { rolesColumns } from "./tables/roles-col";
import { RolesToolbar } from "./tables/roles-toolbar";

import { Button } from "../ui/button";
import { groupColumns } from "./tables/groups-col";

function getDummyUserData() {
  return Array.from({ length: 5 }).map(() => ({
    image: "/placeholder-avatar.png",
    name: `Max`,
    role: `Admin`,
    group: "group-2",
  }));
}

function getDummyEventTypeData() {
  return Array.from({ length: 5 }).map(() => ({
    image: "/placeholder-avatar.png",
    eventTypeName: `Event Type`,
    group: "group-2",
  }));
}

function getDummyGroupData() {
  return Array.from({ length: 5 }).map(() => ({
    image: "/placeholder-avatar.png",
    name: `Max`,
    role: `Admin`,
    group: "group-2",
  }));
}

export function AdminSettings() {
  const userData = getDummyUserData();
  const eventTypeData = getDummyEventTypeData();
  const groupData = getDummyGroupData();

  return (
    <section className="mt-8 w-full rounded-md bg-white p-8 shadow-sm">
      <Tabs defaultValue="roles" className="mt-6">
        <TabsList className="bg-inherit">
          <TabsTrigger
            value="roles"
            className="px-4 data-[state=active]:border-2  data-[state=active]:border-primary data-[state=active]:bg-inherit data-[state=active]:shadow-none"
          >
            Roles
          </TabsTrigger>
          <TabsTrigger
            value="eventTypes"
            className="px-4 data-[state=active]:border-2  data-[state=active]:border-primary data-[state=active]:bg-inherit data-[state=active]:shadow-none"
          >
            Event Types
          </TabsTrigger>
          <TabsTrigger
            value="groups"
            className="px-4 data-[state=active]:border-2  data-[state=active]:border-primary data-[state=active]:bg-inherit data-[state=active]:shadow-none"
          >
            Groups
          </TabsTrigger>
        </TabsList>
        <TabsContent value="roles">
          <div className="mt-10 w-full max-w-[900px] rounded-lg border bg-white p-8 shadow-sm">
            <h2 className="mb-4 text-2xl font-semibold">User Roles</h2>
            <DataTable
              data={userData}
              columns={rolesColumns}
              toolbar={RolesToolbar}
            />
          </div>
        </TabsContent>
        <TabsContent value="eventTypes">
          <div className="mt-10 w-full max-w-[900px] rounded-lg border bg-white p-8 shadow-sm">
            <div className="flex w-full items-center justify-between">
              <h2 className="mb-4 text-2xl font-semibold">
                Event Type Management
              </h2>
              <Button>Add Event Type</Button>
            </div>
            <DataTable
              data={eventTypeData}
              columns={eventTypesColumns}
              toolbar={"none"}
            />
          </div>
        </TabsContent>
        <TabsContent value="groups">
          <div className="mt-10 w-full max-w-[900px] rounded-lg border bg-white p-8 shadow-sm">
            <div className="flex w-full items-center justify-between">
              <h2 className="mb-4 text-2xl font-semibold">Group Management</h2>
              <Button>Add Group</Button>
            </div>
            <DataTable
              data={groupData}
              columns={groupColumns}
              toolbar={"none"}
            />
          </div>
        </TabsContent>
      </Tabs>
    </section>
  );
}
