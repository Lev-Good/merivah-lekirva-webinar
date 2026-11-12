import { createClient } from "@supabase/supabase-js";

const url = "https://vpyowclsxjfwhwghcfnc.supabase.co";
const key = "sb_publishable_lRSTh1QzqFfdR0EKaG_ECg_UyzWtwVW";
export const supabase = createClient(url, key, {
  auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false },
  global: {
    fetch: (input, init) => {
      const headers = new Headers(init?.headers);
      if (headers.get("Authorization") === "Bearer " + key) headers.delete("Authorization");
      return fetch(input, { ...init, headers });
    },
  },
});
