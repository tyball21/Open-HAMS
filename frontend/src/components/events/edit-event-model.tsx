import { DialogTitle } from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";

import { useState } from "react";
import { DatePickerWithRange } from "../dashboard/date-range-picker";
import { Input } from "../ui/input";
import { Textarea } from "../ui/textarea";
import { TimePicker } from "../ui/time-picker/time-picker-12h";

import { deleteEvent, updateEvent } from "@/api/event";
import { useEvent, useEventTypes, useZoos } from "@/api/queries";
import {
  EventSchema,
  eventSchema,
  transformEventSchema,
} from "@/api/schemas/event";
import { EventWithDetails } from "@/utils/types";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { LoadingDots, Spinner } from "../icons";
import {
  AlertDialog,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "../ui/alert-dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { AnimalsSelect } from "./animals-select";
import { HandlerSelect } from "./handlers-select";

export function EditEventFormWrapper({
  eventId,
  setOpen,
}: {
  eventId: string;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const eventDetails = useEvent(eventId);
  if (eventDetails.isLoading) return <LoadingDots className="size-4" />;

  return <EditEventForm eventDetails={eventDetails.data!} />;
}

export function EditEventForm({
  eventDetails,
}: {
  eventDetails: EventWithDetails;
}) {
  const form = useForm<EventSchema>({
    resolver: zodResolver(eventSchema),
    defaultValues: {
      name: eventDetails.event.name,
      description: eventDetails.event.description,
      date: {
        from: new Date(eventDetails.event.start_at),
        to: new Date(eventDetails.event.end_at),
      },
      startTime: new Date(eventDetails.event.start_at),
      endTime: new Date(eventDetails.event.end_at),
      event_type_id: eventDetails.event_type.id.toString(),
      zoo_id: eventDetails.event.zoo_id.toString(),
    },
  });

  const { data: eventTypes, isLoading: isLoadingEventTypes } = useEventTypes();
  const { data: zoos, isLoading: isLoadingZoos } = useZoos();

  const navigate = useNavigate();

  const queryClient = useQueryClient();

  const [selectedAnimals, setSelectedAnimals] = useState<string[]>(
    eventDetails.animals.map((animal) => animal.id.toString()) ?? [],
  );
  const [selectedHandlers, setSelectedHandlers] = useState<string[]>(
    eventDetails.users.map((user) => user.id.toString()) ?? [],
  );
  const [checkoutImmediately, setCheckoutImmediately] =
    useState<boolean>(false);

  if (isLoadingEventTypes || isLoadingZoos) {
    return <LoadingDots className="size-4" />;
  }

  const onSubmit = async (values: EventSchema) => {
    const eventData = transformEventSchema(values);
    const data = {
      event: eventData,
      animal_ids: selectedAnimals,
      user_ids: selectedHandlers,
      checkout_immediately: checkoutImmediately,
    };

    console.log(data);

    const res = await updateEvent(data, eventDetails.event.id.toString());
    if (res.status === 200) {
      toast.success("Event updated successfully");
      queryClient.invalidateQueries({
        queryKey: ["events", eventDetails.event.id],
      });
      queryClient.invalidateQueries({
        queryKey: ["events"],
      });
    } else {
      toast.error(res.data.detail);
    }
  };

  return (
    <>
      <DialogTitle className="mb-3 text-center">Edit Event</DialogTitle>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="flex gap-8">
          <div className="grid w-80 gap-6">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="Enter event name" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="date"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Date</FormLabel>
                  <FormControl>
                    <DatePickerWithRange
                      className="w-full"
                      date={field.value}
                      setDate={field.onChange}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            {/* <div className="flex items-center justify-between gap-8"> */}
            <FormField
              control={form.control}
              name="startTime"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Start Time</FormLabel>
                  <FormControl>
                    <TimePicker date={field.value} setDate={field.onChange} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="endTime"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>End Time</FormLabel>
                  <FormControl>
                    <TimePicker date={field.value} setDate={field.onChange} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description</FormLabel>
                  <FormControl>
                    <Textarea
                      {...field}
                      placeholder="Enter event description"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
          <div className="flex flex-col gap-4">
            <div className="grid w-72 gap-4 rounded-lg bg-[#E5EEF5] p-4">
              <div className="grid gap-2">
                <HandlerSelect
                  selectedHandlers={selectedHandlers}
                  setSelectedHandlers={setSelectedHandlers}
                />
                <AnimalsSelect
                  selectedAnimals={selectedAnimals}
                  setSelectedAnimals={setSelectedAnimals}
                />
              </div>
              {/* <div className="flex items-center justify-between">
                <Label className="text-sm">Check out immediately</Label>
                <Switch
                  checked={checkoutImmediately}
                  onCheckedChange={setCheckoutImmediately}
                />
              </div> */}
            </div>
            <FormField
              control={form.control}
              name="event_type_id"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Event Type</FormLabel>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger className="w-40">
                        <SelectValue />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {eventTypes?.map((eventType) => (
                        <SelectItem
                          key={eventType.id}
                          value={eventType.id.toString()}
                        >
                          {eventType.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="zoo_id"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Zoo</FormLabel>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger className="w-40">
                        <SelectValue placeholder="Select Zoo" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {zoos?.map((zoo) => (
                        <SelectItem key={zoo.id} value={zoo.id.toString()}>
                          {zoo.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="my-4 flex w-full items-center justify-start">
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button variant="destructive" className="w-full" size="sm">
                    Delete Event
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>
                      Are you absolutely sure?
                    </AlertDialogTitle>
                    <AlertDialogDescription>
                      This action cannot be undone. This will permanently delete
                      the event.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <Button
                      variant="destructive"
                      onClick={async () => {
                        const res = await deleteEvent(
                          eventDetails.event.id.toString(),
                        );
                        if (res.status === 200) {
                          toast.success("Event deleted successfully");
                          queryClient.invalidateQueries({
                            queryKey: ["events"],
                          });
                          navigate("/dashboard");
                        } else {
                          toast.error(res.data.detail);
                        }
                      }}
                    >
                      Delete
                    </Button>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
            <div className="mt-auto flex justify-end">
              <Button disabled={form.formState.isSubmitting}>
                {form.formState.isSubmitting ? (
                  <Spinner className="mr-2 size-4" />
                ) : null}
                Save
              </Button>
            </div>
          </div>
        </form>
      </Form>
    </>
  );
}
