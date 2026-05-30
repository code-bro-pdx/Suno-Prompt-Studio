// Lightweight client-side banned word check used to highlight LYRICS inline.
import { useEffect, useState } from "react";
import sunoApi from "@/lib/api";

let cached = null;
let inFlight = null;

export function useKnowledge() {
  const [data, setData] = useState(cached);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (cached) {
      setData(cached);
      return;
    }
    if (!inFlight) {
      inFlight = sunoApi.knowledge().then((d) => {
        cached = d;
        return d;
      });
    }
    inFlight
      .then((d) => setData(d))
      .catch((e) => setError(e));
  }, []);

  return { data, error };
}
