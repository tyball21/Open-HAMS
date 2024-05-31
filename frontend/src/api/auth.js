import { API_URL } from "@/lib/utils";

export async function login(values) {
  const response = await fetch(`${API_URL}/users/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json",
    },
    body: new URLSearchParams(values).toString(),
  });

  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.message);
  }

  return response.json();
}

export async function signup(values) {
  const response = await fetch(`${API_URL}/users/`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(values),
  });

  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.message);
  }

  return response.json();
}
