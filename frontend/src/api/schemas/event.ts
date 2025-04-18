import { addDays } from "date-fns";
import * as z from "zod";

export const eventSchema = z.object({
  name: z
    .string({ message: "Please enter a name" })
    .min(3, "Name is too short"),
  description: z
    .string({ message: "Please enter a description" })
    .min(10, "Description must be at least 10 characters")
    .optional()
    .or(z.literal('')),
  date: z
    .object(
      {
        from: z.date(),
        to: z.date().optional(),
      },
      { required_error: "Please select a date range" },
    )
    .refine((date) => {
      return !!date.to;
    }, "End Date is required.")
    .refine((data) => data.from <= data.to!, {
      message: "Ending date must be after starting date",
    })
    .refine((data) => data.from > addDays(new Date(), -1), {
      message: "Starting date must be in the future",
    })
    .refine((data) => data.to! > addDays(new Date(), -1), {
      message: "Ending date must be in the future",
    }),
  startTime: z.date({ message: "Please select a time" }),
  endTime: z.date({ message: "Please select a time" }),
  zoo_id: z.string({ message: "Please select a zoo" }),
  event_type_id: z.string({ message: "Please select an event type" }),
});

export function transformEventSchema(data: EventSchema) {
  // Combine date.from and startTime into start_at
  const start_at = new Date(
    data.date.from.getFullYear(),
    data.date.from.getMonth(),
    data.date.from.getDate(),
    data.startTime.getHours(),
    data.startTime.getMinutes(),
    data.startTime.getSeconds(),
  );

  // Combine date.to and endTime into end_at
  const end_at = new Date(
    data.date.to!.getFullYear(),
    data.date.to!.getMonth(),
    data.date.to!.getDate(),
    data.endTime.getHours(),
    data.endTime.getMinutes(),
    data.endTime.getSeconds(),
  );

  return {
    name: data.name,
    description: data.description,
    zoo_id: data.zoo_id,
    event_type_id: data.event_type_id,
    start_at,
    end_at,
  };
}

export type EventSchema = z.infer<typeof eventSchema>;
export type TrasformedEventSchema = ReturnType<typeof transformEventSchema>;
