import { User, UserWithEvents } from "@/utils/types";
import instance from "./axios";
import { ChangePasswordSchema, UpdateProfileSchema } from "./schemas/auth";

export async function getAuthenticatedUser(): Promise<User> {
  const res = await instance.get("/users/me");
  console.log(res.data);

  if (res.status === 401) {
    localStorage.removeItem("token");
    if (window.location.href !== "/") window.location.href = "/";
  }

  return res.data as User;
}

export async function updateProfile(values: UpdateProfileSchema) {
  const res = await instance.put(`/users/me`, values);
  return res;
}

export async function changePassword(data: ChangePasswordSchema) {
  const res = await instance.put(`/users/me/password`, data);
  return res;
}

// Add the missing updatePassword alias for backwards compatibility
export async function updatePassword(data: ChangePasswordSchema) {
  return changePassword(data);
}

// Add the missing updateUser function
export async function updateUser(data: UpdateProfileSchema) {
  return updateProfile(data);
}

export async function getUsers() {
  const res = await instance.get("/users/");
  console.log(res.data);
  return res.data as User[];
}

export async function getUser(userId: number) {
  const res = await instance.get(`/users/${userId}`);
  return res.data as UserWithEvents;
}

export async function updateRole(userId: number, role: string) {
  const res = await instance.put(`/users/${userId}/role`, { name: role });
  return res;
}

export async function updateTier(userId: number, tier: number) {
  const res = await instance.put(`/users/${userId}/tier`, { tier });
  return res;
}

export async function updateGroup(userId: number, groupId: number | null) {
  const res = await instance.put(
    `/users/${userId}/group${groupId ? `?group_id=${groupId}` : ""}`
  );
  return res;
}

export async function getHandlers() {
  const res = await instance.get("/users/handlers");
  console.log(res.data);
  return res.data as User[];
}
