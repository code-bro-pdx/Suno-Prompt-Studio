import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API_BASE = `${BACKEND_URL}/api`;

const client = axios.create({
  baseURL: API_BASE,
  timeout: 180000,
  headers: { "Content-Type": "application/json" },
});

export const sunoApi = {
  knowledge: () => client.get("/knowledge").then((r) => r.data),
  generate: (concept, autoRepair = true) =>
    client.post("/generate", { concept, auto_repair: autoRepair }).then((r) => r.data),
  assemble: (form, autoRepair = true) =>
    client.post("/assemble", { form, auto_repair: autoRepair }).then((r) => r.data),
  fillForm: (concept) =>
    client.post("/fill-form", { concept }).then((r) => r.data),
  validate: (payload) =>
    client.post("/validate", { payload }).then((r) => r.data),
  library: {
    list: () => client.get("/library").then((r) => r.data),
    create: (body) => client.post("/library", body).then((r) => r.data),
    get: (id) => client.get(`/library/${id}`).then((r) => r.data),
    delete: (id) => client.delete(`/library/${id}`).then((r) => r.data),
  },
};

export default sunoApi;
