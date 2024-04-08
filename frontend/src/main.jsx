import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import "./index.css";
import { AnimalsPage } from "./routes/dashboard/animals/page";
import { EventsPage } from "./routes/dashboard/events/page";
import { DashboardLayout } from "./routes/dashboard/layout";
import { DashboardPage } from "./routes/dashboard/page";
import { RootLayout } from "./routes/layout";
import { LoginPage } from "./routes/page";
import { UsersPage } from "./routes/dashboard/users/page";

const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [
      { path: "/", element: <LoginPage /> },
      {
        element: <DashboardLayout />,
        children: [
          { path: "/dashboard", element: <DashboardPage /> },
          { path: "/animals", element: <AnimalsPage /> },
          { path: "/events", element: <EventsPage /> },
          { path: "/users", element: <UsersPage /> },
        ],
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);
