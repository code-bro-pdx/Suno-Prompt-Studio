import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API_BASE = `${BACKEND_URL}/api`;

const client = axios.create({
  baseURL: API_BASE,
  timeout: 55000, // stay under k8s ingress 60s cap
  headers: { "Content-Type": "application/json" },
});

// Poll a job until status is done | error, or timeout.
async function pollJob(jobId, { intervalMs = 2000, timeoutMs = 240000, onProgress } = {}) {
  const start = Date.now();
  let attempt = 0;
  while (Date.now() - start < timeoutMs) {
    await new Promise((r) => setTimeout(r, intervalMs));
    attempt += 1;
    try {
      const { data } = await client.get(`/jobs/${jobId}`);
      if (onProgress) onProgress(data, attempt);
      if (data.status === "done") return data.result;
      if (data.status === "error") throw new Error(data.error || "Job failed");
    } catch (e) {
      // For transient errors (e.g., one-off 502), retry up to 3 times
      if (attempt > 3 && Date.now() - start > 30000) throw e;
    }
  }
  throw new Error("Job timed out");
}

export const sunoApi = {
  knowledge: () => client.get("/knowledge").then((r) => r.data),
  generate: async (concept, autoRepair = true, opts = {}) => {
    const { data } = await client.post("/generate", { concept, auto_repair: autoRepair });
    return pollJob(data.job_id, opts);
  },
  assemble: async (form, autoRepair = true, opts = {}) => {
    const { data } = await client.post("/assemble", { form, auto_repair: autoRepair });
    return pollJob(data.job_id, opts);
  },
  fillForm: (concept) =>
    client.post("/fill-form", { concept }).then((r) => r.data),
  validate: (payload) =>
    client.post("/validate", { payload }).then((r) => r.data),
  jobs: {
    get: (id) => client.get(`/jobs/${id}`).then((r) => r.data),
  },
  library: {
    list: () => client.get("/library").then((r) => r.data),
    create: (body) => client.post("/library", body).then((r) => r.data),
    get: (id) => client.get(`/library/${id}`).then((r) => r.data),
    delete: (id) => client.delete(`/library/${id}`).then((r) => r.data),
  },
};

export default sunoApi;
