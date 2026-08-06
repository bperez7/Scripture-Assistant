const API_BASE_URL = "http://localhost:8000";

export async function askQuestion(question) {
  const response = await fetch(`${API_BASE_URL}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("Failed to ask question");
  }

  return response.json();
}

export async function searchScriptures(query) {
  const response = await fetch(
    `${API_BASE_URL}/scriptures/search?q=${encodeURIComponent(query)}`
  );

  if (!response.ok) {
    throw new Error("Failed to search scriptures");
  }

  return response.json();
}