import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import "./index.css";
import { RootLayout } from "./routes/layout";
import { DashboardPage } from "./routes/page";

const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [{ path: "/", element: <DashboardPage /> }],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);
