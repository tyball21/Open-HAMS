import { GeneralSettings } from "@/components/settings/general";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export function SettingsPage() {
  return (
    <main>
      <h1 className="mt-6 text-2xl font-bold">Settings</h1>
      <Tabs defaultValue="general" className="mt-6">
        <TabsList className="bg-[#E6EEF5]">
          <TabsTrigger
            value="general"
            className="data-[state=active]:bg-primary px-6"
          >
            General
          </TabsTrigger>
          <TabsTrigger
            value="adminPermissions"
            className="data-[state=active]:bg-primary px-6"
          >
            Admin Permissions
          </TabsTrigger>
          <TabsTrigger
            value="reports"
            className="data-[state=active]:bg-primary px-6"
          >
            Reports
          </TabsTrigger>
        </TabsList>
        <TabsContent value="general">
            <GeneralSettings />
        </TabsContent>
        <TabsContent value="adminPermissions">Admin Permissions</TabsContent>
        <TabsContent value="reports">Reports</TabsContent>
      </Tabs>
    </main>
  );
}
