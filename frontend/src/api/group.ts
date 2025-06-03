import { Group } from "@/utils/types";
import instance from "./axios";
import { GroupSchema } from "./schemas/group";

export async function createGroup(values: GroupSchema) {
  const res = await instance.post("/groups/", values);
  return res;
}

export async function getGroups(): Promise<Group[]> {
  const res = await instance.get("/groups/");
  return res.data as Group[];
}
