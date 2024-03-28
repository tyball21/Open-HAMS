import { cn } from "@/lib/utils";
import { Activity, Dog, LayoutDashboard } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";

export function Sidebar() {
  return (
    <aside className="hidden h-full w-56 flex-col bg-background p-4 lg:flex">
      <div className="flex items-center gap-2">
        <img src="/logo.png" alt="logo" className="size-7" />
        <h1 className="text-[20px] font-bold tracking-tight">Open HAMS</h1>
      </div>
      <nav className="mt-16 space-y-1">
        <SidebarItem title="Dashboard" icon={LayoutDashboard} active />
        <SidebarItem title="Animals" icon={Dog} />
        <SidebarItem title="Events" icon={Activity} />
      </nav>
      <div className="mb-2 mt-auto flex gap-2">
        <Avatar>
          <AvatarImage src="https://github.com/shadcn.png" />
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>
        <div className="flex flex-col">
          <span className="text-[14px] font-bold">John Doe</span>
          <span className="text-[12px] text-muted-foreground">
            Account Settings
          </span>
        </div>
      </div>
    </aside>
  );
}

function SidebarItem({ title, icon: Icon, active }) {
  return (
    <div
      className={cn(
        "flex items-center gap-3 rounded-md p-2",
        active ? "bg-muted" : "hover:bg-muted",
      )}
    >
      <Icon className="size-4 font-bold text-[#374151] dark:text-white" />
      <span className="text-[14px] text-muted-foreground">{title}</span>
    </div>
  );
}
