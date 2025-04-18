import { useUser } from "@/api/queries";
import { AdminSettings } from "@/components/settings/admin";
import { GeneralSettings } from "@/components/settings/general";
import { ReportsSettings } from "@/components/settings/reports";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Loading } from "@/routes/loading";
import { Heart } from "lucide-react";
import { useSearchParams } from "react-router-dom";

export function SettingsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const { data: user, isLoading } = useUser();

  if (isLoading) {
    return <Loading />;
  }

  return (
    <main>
      <h1 className="mt-6 text-2xl font-bold">Settings</h1>
      <Tabs
        value={searchParams.get("tab") || "general"}
        className="mt-6"
        onValueChange={(value) => {
          setSearchParams({ tab: value });
        }}
      >
        <div className="flex w-full items-center flex-col lg:flex-row gap-4 justify-start lg:justify-between">
          <TabsList className="bg-[#E6EEF5]">
            <TabsTrigger
              value="general"
              className="px-6 data-[state=active]:bg-primary"
            >
              General
            </TabsTrigger>
            {/* Only show these tabs to admin */}
            {user?.role?.name === "admin" && (
              <>
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
              </>
            )}
          </TabsList>
          <div className="flex items-center gap-2">
            <p className="text-sm">Built by: </p>
            <p>Open HAMS</p>
            <Heart className="size-6" />
            <p>Utah's Hogle Zoo</p>
          </div>
        </div>
        <TabsContent value="general">
          <GeneralSettings />
        </TabsContent>
        {/* Only show these tabs to admin */}
        {user?.role?.name === "admin" && (
          <>
            <TabsContent value="adminPermissions">
              <AdminSettings />
            </TabsContent>
            <TabsContent value="reports">
              <ReportsSettings />
            </TabsContent>
          </>
        )}
      </Tabs>
    </main>
  );
}
