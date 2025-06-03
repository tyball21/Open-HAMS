import * as z from "zod";

export const animalSchema = z.object({
  name: z.string().min(2, "Name must be between 2 and 50 characters").max(50),
  species: z
    .string()
    .min(2, "Species must be between 2 and 50 characters")
    .max(50),
  description: z
    .string()
    .max(500)
    .optional()
    .or(z.literal('')),
  image: z.any().optional(),
  handling_enabled: z.boolean(),
  max_daily_checkout_hours: z.preprocess(
    (val) => (val === '' || val == null ? 0 : Number(val)),
    z.number().int().nonnegative("Must be 0 or positive").optional()
  ),
  max_daily_checkouts: z.number().int().positive(),
  rest_time: z.preprocess(
    (val) => (val === '' || val == null ? 0 : Number(val)),
    z.number().nonnegative("Must be 0 or positive").optional()
  ),
  tier: z.string({ message: "Tier is required" }),
  zoo_id: z.string({ message: "Zoo is required" }),
});

export const animalHealthLogSchema = z.object({
  details: z
    .string({ message: "Details are required" })
    .min(10, "Details must be more than 10 characters"),
});

export type AnimalSchema = z.infer<typeof animalSchema>;
export type AnimalHealthLogSchema = z.infer<typeof animalHealthLogSchema>;
