import { AdminSettings } from "@/components/settings/admin";
import { GeneralSettings } from "@/components/settings/general";
import { ReportsSettings } from "@/components/settings/reports";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export function SettingsPage() {
  return (
    <main>
      <h1 className="mt-6 text-2xl font-bold">Settings</h1>
      <Tabs defaultValue="general" className="mt-6">
        <TabsList className="bg-[#E6EEF5]">
          <TabsTrigger
            value="general"
            className="px-6 data-[state=active]:bg-primary"
          >
            General
          </TabsTrigger>
          <TabsTrigger
            value="adminPermissions"
            className="px-6 data-[state=active]:bg-primary"
          >
            Admin Permissions
          </TabsTrigger>
          <TabsTrigger
            value="reports"
            className="px-6 data-[state=active]:bg-primary"
          >
            Reports
          </TabsTrigger>
        </TabsList>
        <TabsContent value="general">
          <GeneralSettings />
        </TabsContent>
        <TabsContent value="adminPermissions">
          <AdminSettings />
        </TabsContent>
        <TabsContent value="reports">
          <ReportsSettings />
        </TabsContent>
      </Tabs>
    </main>
  );
}
