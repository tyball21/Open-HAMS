import { addDays, isToday, isFuture, isBefore, isAfter, startOfToday } from "date-fns";
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
    .refine((data) => {
      // Allow future dates unconditionally
      if (isFuture(data.from) && !isToday(data.from)) {
        return true;
      }
      
      // For today, we'll validate the actual start time when combined with the selected time
      if (isToday(data.from)) {
        return true; // We'll validate the full date+time combination separately
      }
      
      return false;
    }, "Starting date must be today or in the future")
    .refine((data) => {
      // Allow future dates unconditionally for end date
      if (isFuture(data.to!) && !isToday(data.to!)) {
        return true;
      }
      
      // For today, we'll validate the combined date+time
      if (isToday(data.to!)) {
        return true;
      }
      
      return false;
    }, "Ending date must be today or in the future"),
  startTime: z.date({ message: "Please select a time" }),
  endTime: z.date({ message: "Please select a time" }),
  zoo_id: z.string({ message: "Please select a zoo" }),
  event_type_id: z.string({ message: "Please select an event type" }),
}).superRefine((data, ctx) => {
  // Only evaluate this for same-day events
  if (isToday(data.date.from) && data.startTime) {
    // Create a full date+time object for comparison
    const now = new Date();
    const eventStart = new Date(
      data.date.from.getFullYear(),
      data.date.from.getMonth(),
      data.date.from.getDate(),
      data.startTime.getHours(),
      data.startTime.getMinutes(),
      data.startTime.getSeconds(),
    );
    
    // For same-day events, ensure the start time is in the future
    if (isBefore(eventStart, now)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "For events today, start time must be in the future",
        path: ["startTime"],
      });
    }
  }
  
  // Validate that for same-day events, end time is after start time
  if (data.date.from && data.date.to && 
      data.date.from.getTime() === data.date.to.getTime() &&
      data.startTime && data.endTime) {
    
    if (data.endTime <= data.startTime) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "End time must be after start time for same-day events",
        path: ["endTime"],
      });
    }
  }
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
