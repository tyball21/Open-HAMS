import { cn } from "@/lib/utils";
import { Activity, Dog, LayoutDashboard, User } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";

import { useMemo } from "react";
import { Link, useLocation } from "react-router-dom";
import { Search } from "./ui/input";

export function Sidebar() {
  const location = useLocation();

  const routes = useMemo(() => {
    return [
      {
        title: "Dashboard",
        icon: LayoutDashboard,
        path: "/dashboard",
        active: location.pathname === "/dashboard",
      },
      {
        title: "Animals",
        icon: Dog,
        path: "/animals",
        active: location.pathname === "/animals",
      },
      {
        title: "Events",
        icon: Activity,
        path: "/events",
        active: location.pathname === "/events",
      },
      {
        title: "Users",
        icon: User,
        path: "/users",
        active: location.pathname === "/users",
      },
    ];
  }, [location.pathname]);

  return (
    <aside className="flex h-screen w-full flex-col bg-background p-4 border-r">
      <Link className="flex items-center gap-2" to="/">
        <img src="/logo.png" alt="logo" className="size-7" />
        <h1 className="text-[20px] font-bold tracking-tight">Open HAMS</h1>
      </Link>
      <Search placeholder="Search..." className="mt-16" />
      <nav className="mt-4 space-y-1">
        {routes.map((route) => (
          <SidebarItem key={route.path} {...route} />
        ))}
      </nav>
      <div className="mb-2 mt-auto flex gap-2">
        <Avatar>
          <AvatarImage src="https://github.com/ahmedivy.png" />
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

function SidebarItem({ title, icon: Icon, active, path }) {
  return (
    <Link
      to={path}
      className={cn(
        "flex items-center gap-3 rounded-md p-2",
        active ? "bg-muted" : "hover:bg-muted",
      )}
    >
      <Icon className="size-4 font-bold text-[#374151] dark:text-white" />
      <span className="text-[14px] text-muted-foreground">{title}</span>
    </Link>
  );
}
