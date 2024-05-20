import { zodResolver } from "@hookform/resolvers/zod";
import { Heart } from "lucide-react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { signup } from "@/lib/auth";
import { toast } from "sonner";

export function SignUpPage() {
  const formSchema = z.object({
    first_name: z.string().min(2).max(50),
    last_name: z.string().optional(),
    username: z.string().min(2).max(50),
    email: z.string().email(),
    password: z.string().min(8).max(50),
  });

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
      email: "",
      first_name: "",
      last_name: "",
    },
  });

  function onSubmit(values) {
    console.log(values);

    toast.promise(
      async () => {
        try {
          var data = await signup(values);
        } catch (error) {
          throw new Error(error.message);
        }

        console.log(data);
      },
      {
        loading: "Signing Up...",
        success: "Account created successfully",
        error: (data) => {
          return data.message || "Something went wrong";
        },
      },
    );
  }

  return (
    <body className="flex min-h-screen flex-col bg-blueish">
      <div className="container grid h-full flex-1 grid-cols-1 px-4 lg:grid-cols-2 lg:py-24">
        <img
          src="serenity.png"
          alt="Scence Image"
          className="hidden h-full rounded-xl lg:block"
        />
        <div className="flex flex-col items-center px-4 py-8 lg:px-32">
          <img src="logo.png" alt="Logo" className="size-28" />
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="mt-8 w-full space-y-8 lg:mt-16"
            >
              <div className="grid w-full gap-3 md:grid-cols-2">
                <FormField
                  control={form.control}
                  name="first_name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>First Name</FormLabel>
                      <FormControl>
                        <Input {...field} placeholder="Enter your first name" />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="last_name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Last Name</FormLabel>
                      <FormControl>
                        <Input {...field} placeholder="Enter your last name" />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input {...field} placeholder="Enter your email" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="username"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Username</FormLabel>
                    <FormControl>
                      <Input {...field} placeholder="Enter your username" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        placeholder="Enter your password"
                        type="password"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" className="w-full">
                Sign Up
              </Button>
            </form>
          </Form>
          <p className="mt-4">or</p>
          <Button
            className="mt-4 w-full"
            variant="secondary"
            onClick={() => {
              toast.error("Login with Google is not avaiable yet");
            }}
          >
            Sign Up with Google
          </Button>
          <p className="mt-6 self-start text-sm">
            Already a member?
            <Link to="/" className="ml-1  underline">
              Log In
            </Link>
          </p>
        </div>
      </div>
      <footer className="mt-auto flex flex-col gap-2 border-t-2 border-white p-2 px-4 lg:p-4 lg:px-24">
        <div className="flex items-center gap-2">
          <p>Open HAMS</p>
          <Heart className="size-6" />
          <p>Hogle Zoo</p>

          <Link to="/dashboard" className="ml-auto">
            home
          </Link>
        </div>
        <div className="flex items-center gap-2 border-t pt-2">
          <p className="text-[#059669]">© 2024 Eleganza Homes</p>
          <Link to="/terms" className="ml-auto text-[#064E3B]">
            Terms
          </Link>
          <Link to="/terms" className="ml-4 text-[#064E3B]">
            Privacy
          </Link>
        </div>
      </footer>
    </body>
  );
}
