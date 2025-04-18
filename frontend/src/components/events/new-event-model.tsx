import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";

import { Plus } from "lucide-react";
import { useState } from "react";
import { DatePickerWithRange } from "../dashboard/date-range-picker";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Switch } from "../ui/switch";
import { Textarea } from "../ui/textarea";
import { TimePicker } from "../ui/time-picker/time-picker-12h";

import { createEvent } from "@/api/event";
import {
  useAnimalStatus,
  useEventTypes,
  useHandlers,
  useZoos,
} from "@/api/queries";
import {
  EventSchema,
  eventSchema,
  transformEventSchema,
} from "@/api/schemas/event";
import { getInitials } from "@/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useQueryClient } from "react-query";
import { toast } from "sonner";
import { LoadingDots, Spinner } from "../icons";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
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
import { AvatarWithTooltip } from "./avatar-with-tooltip";
import { CustomSelect } from "./custom-select";
import { AnimalStatus } from "@/api/animals";
import { User, EventType, Zoo } from "@/utils/types";

export function NewEventModel() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger>
        <Button className="ml-auto">
          <Plus className="mr-2 size-4" />
          Create New Event
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-fit">
        <NewEventCard setOpen={setOpen} />
      </DialogContent>
    </Dialog>
  );
}

export function NewEventCard({
  setOpen,
}: {
  setOpen?: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const form = useForm<EventSchema>({
    resolver: zodResolver(eventSchema),
    defaultValues: {},
  });
  const queryClient = useQueryClient();

  const { data: eventTypes, isLoading: isLoadingEventTypes } = useEventTypes();
  const { data: zoos, isLoading: isLoadingZoos } = useZoos();
  const { data: handlers, isLoading: isLoadingHandlers } = useHandlers();
  const { data: animals, isLoading: isLoadingAnimals } = useAnimalStatus(
    form.getValues("zoo_id"),
  );

  const [selectedAnimals, setSelectedAnimals] = useState<string[]>([]);
  const [selectedHandlers, setSelectedHandlers] = useState<string[]>([]);
  const [checkoutImmediately, setCheckoutImmediately] =
    useState<boolean>(false);

  if (
    isLoadingEventTypes ||
    isLoadingZoos ||
    isLoadingHandlers ||
    isLoadingAnimals
  ) {
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
    const res = await createEvent(data);
    if (res.status === 200) {
      form.reset();
      toast.success("Event created successfully");
      setOpen?.(false);
      queryClient.invalidateQueries({
        queryKey: ["events"],
      });
    } else {
      toast.error(res.data.detail);
    }
  };

  return (
    <div className="max-w-fit">
      <h2 className="mb-3 text-center">Create New Event</h2>
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
                <CustomSelect
                  label="Handlers"
                  placeholder="Search handlers"
                  options={handlers!.map((handler: User) => ({
                    value: handler.id.toString(),
                    label: `${handler.first_name} ${handler.last_name}`,
                    toRender: (
                      <>
                        <Avatar className="size-5">
                          <AvatarImage src={handler.image!} />
                          <AvatarFallback>
                            {getInitials(handler.first_name, handler.last_name)}
                          </AvatarFallback>
                        </Avatar>
                        <span className="font-extralightlight text-xs text-foreground">
                          {`${handler.first_name} ${handler.last_name}`}
                        </span>
                        <span className="ml-auto text-xs text-foreground">
                          {handler?.role?.name}
                        </span>
                      </>
                    ),
                  }))}
                  selected={selectedHandlers}
                  setSelected={setSelectedHandlers}
                  listElement={({ value }: { value: string }) => {
                    const handler = handlers!.find((h: User) => h.id.toString() === value);
                    return (
                      <AvatarWithTooltip
                        src={handler?.image!}
                        name={handler?.first_name + " " + handler?.last_name}
                      >
                        <div className="flex items-center gap-2">
                          <Avatar className="size-8">
                            <AvatarImage src={handler?.image!} />
                            <AvatarFallback>
                              {getInitials(
                                handler?.first_name!,
                                handler?.last_name,
                              )}
                            </AvatarFallback>
                          </Avatar>
                          <span className="text-md font-semibold">
                            {handler?.first_name} {handler?.last_name}
                          </span>
                          <Button
                            className="ml-auto"
                            size={"xs"}
                            onClick={(e) => {
                              e.preventDefault();

                              setSelectedHandlers((prev) =>
                                prev.filter((id) => id !== value),
                              );
                            }}
                          >
                            Remove
                          </Button>
                        </div>
                        <div className="mt-2 flex items-center gap-2">
                          <Label className="text-xs font-semibold">
                            Email:
                          </Label>
                          <span className="text-xs">{handler?.email}</span>
                        </div>
                        <div className="mt-2 flex items-center gap-2">
                          <Label className="text-xs font-semibold">Zoo:</Label>
                          <span className="text-xs">{handler?.zoo?.name}</span>
                        </div>
                      </AvatarWithTooltip>
                    );
                  }}
                />
                <CustomSelect
                  label="Animals"
                  placeholder="Search animals"
                  options={animals!.map((animal_info: AnimalStatus) => ({
                    value: animal_info.animal.id.toString(),
                    label: animal_info.animal.name,
                    toRender: (
                      <>
                        <Avatar className="size-5">
                          <AvatarImage src={animal_info.animal.image_filename ? `/static/animal_images/${animal_info.animal.image_filename}` : undefined} />
                          <AvatarFallback>
                            {getInitials(animal_info.animal.name)}
                          </AvatarFallback>
                        </Avatar>
                        <span className="font-extralightlight text-xs text-foreground">
                          {animal_info.animal.name}
                        </span>
                        <span className="ml-auto">
                          {animal_info.status === "available" ? (
                            <div className="flex items-center gap-2">
                              <span className="text-green-400">Available</span>
                            </div>
                          ) : animal_info.status === "unavailable" ? (
                            <div className="flex items-center">
                              <span>Unavailable</span>
                              <span className="w-[30px] text-wrap text-start text-[8px] leading-tight">
                                {animal_info.status_description}
                              </span>
                            </div>
                          ) : (
                            <span className="">Checked Out</span>
                          )}
                        </span>
                      </>
                    ),
                  }))}
                  selected={selectedAnimals}
                  setSelected={setSelectedAnimals}
                  listElement={({ value }: { value: string }) => {
                    const animal = animals!.find(
                      (h: AnimalStatus) => h.animal.id.toString() === value,
                    );
                    return (
                      <AvatarWithTooltip
                        src={animal?.animal.image_filename ? `/static/animal_images/${animal.animal.image_filename}` : ""}
                        name={animal?.animal.name}
                      >
                        <div className="flex items-center gap-2">
                          <Avatar className="size-8">
                            <AvatarImage src={animal?.animal.image_filename ? `/static/animal_images/${animal.animal.image_filename}` : undefined} />
                            <AvatarFallback>
                              {getInitials(animal?.animal.name!)}
                            </AvatarFallback>
                          </Avatar>
                          <span className="text-md font-semibold">
                            {animal?.animal.name}
                          </span>
                          <Button
                            className="ml-auto"
                            size={"xs"}
                            onClick={(e) => {
                              e.preventDefault();

                              setSelectedAnimals((prev) =>
                                prev.filter((id) => id !== value),
                              );
                            }}
                          >
                            Remove
                          </Button>
                        </div>

                        <div className="mt-2 flex items-center gap-2">
                          <Label className="text-xs font-semibold">
                            Status:
                          </Label>
                          <span className="text-xs">
                            {animal?.status_description}
                          </span>
                        </div>
                      </AvatarWithTooltip>
                    );
                  }}
                />
              </div>
              <div className="flex items-center justify-between">
                <Label className="text-sm">Check out immediately</Label>
                <Switch
                  checked={checkoutImmediately}
                  onCheckedChange={setCheckoutImmediately}
                />
              </div>
            </div>
            <FormField
              control={form.control}
              name="event_type_id"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Event Type</FormLabel>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value as any as string}
                  >
                    <FormControl>
                      <SelectTrigger className="w-40">
                        <SelectValue placeholder="Select Event Type" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {eventTypes?.map((eventType: EventType) => (
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
                    defaultValue={field.value as any as string}
                  >
                    <FormControl>
                      <SelectTrigger className="w-40">
                        <SelectValue placeholder="Select Zoo" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {zoos?.map((zoo: Zoo) => (
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
            <div className="mt-auto flex justify-end">
              <Button disabled={form.formState.isSubmitting}>
                {form.formState.isSubmitting ? (
                  <Spinner className="mr-2 size-4" />
                ) : null}
                Create
              </Button>
            </div>
          </div>
        </form>
      </Form>
    </div>
  );
}
