import { Heart } from "lucide-react";
import { Link, Outlet } from "react-router-dom";

export function AuthLayout() {
  return (
    <main className="flex min-h-screen flex-col bg-blueish">
      <div className="grid w-full flex-1 lg:grid-cols-2">
        <div className="flex flex-col items-center justify-center">
          <img
            src="serenity.png"
            alt="Scence Image"
            className="hidden h-3/4  rounded-xl lg:block"
          />
        </div>
        <div className="flex flex-col items-center justify-center px-6 py-12">
          <img src="logo.png" alt="Logo" className="size-28" />
          <Outlet />
        </div>
      </div>
      <footer className="mt-auto flex flex-col gap-2 border-t-2 border-white p-2 px-4 lg:p-4 lg:px-8">
        <div className="flex items-center gap-2">
          <p className="text-sm">Built by: </p>
          <p>Open HAMS</p>
          <Heart className="size-6" />
          <p>Utah's Hogle Zoo</p>

          <Link to="/dashboard" className="ml-auto">
            home
          </Link>
        </div>
        <div className="flex items-center gap-2 border-t pt-2">
          {/* Remove this line below */}
          <Link to="/terms" className="ml-auto text-[#064E3B]">
            Terms
          </Link>
        </div>
      </footer>
    </main>
  );
}
