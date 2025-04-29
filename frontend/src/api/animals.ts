import {
  Animal,
  AnimalAuditWithDetails,
  AnimalFeed,
  AnimalHealthLogWithDetails,
  AnimalWithCurrentEvent,
  AnimalWithEvents,
  RestingAnimal,
} from "@/utils/types";
import instance from "./axios";
import { AnimalHealthLogSchema, AnimalSchema } from "./schemas/animal";

export async function getAnimals() {
  const res = await instance.get("/animals");
  return res.data as Animal[];
}

export async function createAnimal(formData: FormData) {
  const res = await instance.post("/animals", formData);
  return res;
}

export async function updateAnimal(formData: FormData, animalId: string) {
  const res = await instance.put(`/animals/${animalId}`, formData);
  return res;
}

export async function getAnimal(animalId: string) {
  const res = await instance.get(`/animals/${animalId}`);
  if (res.status !== 200) throw new Error(res.data);
  return res.data as Animal;
}

export async function deleteAnimal(animalId: string) {
  const res = await instance.delete(`/animals/${animalId}`);
  return res;
}

export async function getAnimalDetails(animalId: string) {
  const res = await instance.get(`/animals/${animalId}/details`);
  if (res.status !== 200) throw new Error(res.data);
  return res.data as AnimalWithEvents;
}

export type AnimalStatus = {
  animal: Animal;
  status: "available" | "unavailable" | "checked_out";
  status_description: string;
};

export async function getAnimalsWithStatus(zoo_id?: string) {
  const res = await instance.get(
    "/animals/status",
    zoo_id
      ? {
          params: { zoo_id },
        }
      : {},
  );
  return res.data as AnimalStatus[];
}

export async function makeAnimalUnavailable(animalId: string) {
  const res = await instance.put(`/animals/${animalId}/unavailable`);
  return res;
}

export async function makeAnimalAvailable(animalId: string) {
  const res = await instance.put(`/animals/${animalId}/available`);
  return res;
}

export async function getAnimalAuditLog(animalId: string) {
  const res = await instance.get(`/animals/${animalId}/audits`);
  return res.data as AnimalAuditWithDetails[];
}

export async function getAnimalHealthLog(animalId: string) {
  const res = await instance.get(`/animals/${animalId}/health-log`);
  return res.data as AnimalHealthLogWithDetails[];
}

export async function createAnimalHealthLog(
  animalId: string,
  details: AnimalHealthLogSchema,
) {
  const res = await instance.post(`/animals/${animalId}/health-log`, details);
  return res;
}

export async function updateAnimalHealthLog(
  animalId: string,
  logId: string,
  details: AnimalHealthLogSchema,
) {
  const res = await instance.put(
    `/animals/${animalId}/health-log/${logId}`,
    details,
  );
  return res;
}

export async function getCheckedOutAnimals() {
  const res = await instance.get("/animals/details/checkedout");
  return res.data as AnimalWithCurrentEvent[];
}

export async function getRestingAnimals() {
  const res = await instance.get("/animals/details/resting");
  return res.data as RestingAnimal[];
}

export async function getAnimalFeed() {
  const res = await instance.get("/animals/feed");
  return res.data as AnimalFeed[];
}
