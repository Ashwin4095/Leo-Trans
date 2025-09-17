export type GlossaryEntry = {
  id: string;
  source_term: string;
  thai_term: string;
  part_of_speech?: string | null;
  context?: string | null;
  notes?: string | null;
  is_sensitive: boolean;
};

export type GlossaryEntryCreate = {
  source_term: string;
  thai_term: string;
  part_of_speech?: string;
  context?: string;
  notes?: string;
  is_sensitive?: boolean;
};

export type GlossaryListResponse = {
  items: GlossaryEntry[];
  total: number;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || response.statusText);
  }
  return response.json() as Promise<T>;
}

export async function fetchGlossary(search?: string): Promise<GlossaryListResponse> {
  const url = new URL("/glossary", API_BASE_URL);
  if (search) {
    url.searchParams.append("search", search);
  }
  return handleResponse<GlossaryListResponse>(await fetch(url, { cache: "no-store" }));
}

export async function createGlossaryEntry(entry: GlossaryEntryCreate): Promise<GlossaryEntry> {
  const response = await fetch(`${API_BASE_URL}/glossary`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(entry),
  });
  return handleResponse<GlossaryEntry>(response);
}

export async function deleteGlossaryEntry(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/glossary/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || response.statusText);
  }
}

export type SubmissionStatus = "editing" | "in_review" | "approved" | "needs_changes";

export interface Submission {
  id: string;
  title: string;
  source_text: string;
  tone?: string | null;
  audience?: string | null;
  channel?: string | null;
  thai_draft: string;
  thai_final?: string | null;
  translation_prompt?: string | null;
  provider_name?: string | null;
  usage_tokens?: number | null;
  cost_usd?: number | null;
  glossary_terms: string[];
  warnings: string[];
  notes?: string | null;
  status: SubmissionStatus;
  reviewer_notes?: string | null;
  last_reviewed_at?: string | null;
  created_at: string;
  updated_at: string;
}

export type SubmissionCreate = {
  title: string;
  source_text: string;
  tone?: string;
  audience?: string;
  channel?: string;
};

export type SubmissionUpdate = {
  thai_final?: string;
  status?: SubmissionStatus;
  reviewer_notes?: string;
};

export type SubmissionListResponse = {
  items: Submission[];
  total: number;
};

export async function fetchSubmissions(status?: SubmissionStatus): Promise<SubmissionListResponse> {
  const url = new URL("/submissions", API_BASE_URL);
  if (status) {
    url.searchParams.append("status", status);
  }
  return handleResponse<SubmissionListResponse>(await fetch(url, { cache: "no-store" }));
}

export async function fetchSubmission(id: string): Promise<Submission> {
  return handleResponse<Submission>(await fetch(`${API_BASE_URL}/submissions/${id}`, { cache: "no-store" }));
}

export async function createSubmission(payload: SubmissionCreate): Promise<Submission> {
  const response = await fetch(`${API_BASE_URL}/submissions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<Submission>(response);
}

export async function updateSubmission(id: string, payload: SubmissionUpdate): Promise<Submission> {
  const response = await fetch(`${API_BASE_URL}/submissions/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<Submission>(response);
}

export type MetricsOverview = {
  generated_at: string;
  total_submissions: number;
  submissions_by_status: Record<string, number>;
  submissions_with_warnings: number;
  approval_rate: number;
  average_tokens: number | null;
  total_tokens: number;
  total_cost_usd: number;
};

export async function fetchMetricsOverview(days?: number): Promise<MetricsOverview> {
  const url = new URL("/metrics/overview", API_BASE_URL);
  if (days) {
    url.searchParams.append("days", String(days));
  }
  return handleResponse<MetricsOverview>(await fetch(url, { cache: "no-store" }));
}

export async function exportSubmission(id: string, format: "csv" | "docx" | "social"): Promise<void> {
  const url = new URL(`/submissions/${id}/export`, API_BASE_URL);
  url.searchParams.append("format", format);
  const response = await fetch(url.toString());
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || response.statusText);
  }
  const blob = await response.blob();
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  const disposition = response.headers.get("content-disposition") ?? "";
  const match = disposition.match(/filename=([^;]+)/i);
  link.download = match ? match[1] : `submission-${id}.${format === "social" ? "txt" : format}`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(link.href);
}
