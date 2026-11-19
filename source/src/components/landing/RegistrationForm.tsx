import { useState } from "react";
import { z } from "zod";
import { supabase } from "@/integrations/supabase/client";

const emailSources = new Set([
  "email-yuval-internal",
  "hameanyenim",
  "influencer-shevi",
  "influencer-yaakov",
]);

const phone = z.string().trim().regex(/^[0-9+\-\s]{9,15}$/, "נא להזין מספר נייד תקין");
const email = z.string().trim().max(255).email("כתובת הדוא״ל אינה תקינה");
const baseSchema = z.object({
  full_name: z.string().trim().min(2, "נא למלא שם מלא").max(100, "השם ארוך מדי"),
  marketing_consent: z.boolean().default(false),
  consent: z.literal(true, { errorMap: () => ({ message: "יש לאשר כדי להירשם" }) }),
});
const optionalContact = z.string().trim().pipe(z.literal(""));

type Errors = Partial<Record<"full_name" | "phone" | "email" | "consent" | "form", string>>;

export function RegistrationForm({ source = null }: { source?: string | null }) {
  const isProg = source === "prog" || source === "general";
  const [preferredChannel, setPreferredChannel] = useState<"email" | "whatsapp" | "">("");
  const phoneRequired = isProg ? preferredChannel === "whatsapp" : !emailSources.has(source ?? "");
  const emailRequired = isProg ? preferredChannel === "email" : !phoneRequired;
  const [values, setValues] = useState({ full_name: "", phone: "", email: "", consent: false, marketing_consent: false });
  const [errors, setErrors] = useState<Errors>({});
  const [status, setStatus] = useState<"idle" | "sending">("idle");

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (isProg && !preferredChannel) {
      setErrors({ form: "נא לבחור איך תרצו לקבל עדכונים." });
      return;
    }
    const parsed = baseSchema.extend({
      phone: phoneRequired ? phone : phone.or(optionalContact),
      email: emailRequired ? email : email.or(optionalContact),
    }).safeParse({
      ...values,
      phone: isProg && !phoneRequired ? "" : values.phone,
      email: isProg && !emailRequired ? "" : values.email,
    });
    if (!parsed.success) {
      const errs: Errors = {};
      for (const issue of parsed.error.issues) errs[issue.path[0] as keyof Errors] = issue.message;
      setErrors(errs);
      return;
    }
    setErrors({});
    setStatus("sending");
    const { error } = await supabase.from("webinar_registrations").insert({
      full_name: parsed.data.full_name,
      phone: parsed.data.phone || null,
      email: parsed.data.email || null,
      consent: true,
      marketing_consent: parsed.data.marketing_consent,
      source,
    });
    if (error) {
      setStatus("idle");
      setErrors({ form: "משהו השתבש בשליחה. נסו שוב בעוד רגע." });
      return;
    }
    window.location.assign("./thank-you/");
  }

  const field =
    "w-full rounded-2xl border border-input bg-background px-4 py-3 text-base text-brand-ink outline-none transition focus:border-brand-blue focus:ring-2 focus:ring-brand-blue/20";

  return (
    <form onSubmit={onSubmit} noValidate className="space-y-5 rounded-3xl bg-card p-6 shadow-card sm:p-10">
      <div>
        <label htmlFor="full_name" className="mb-1.5 block font-semibold text-brand-blue">
          שם מלא *
        </label>
        <input
          id="full_name"
          className={field}
          autoComplete="name"
          maxLength={100}
          value={values.full_name}
          onChange={(e) => setValues({ ...values, full_name: e.target.value })}
        />
        {errors.full_name && <p className="mt-1 text-sm text-destructive">{errors.full_name}</p>}
      </div>
      {isProg && (
        <fieldset className="space-y-2">
          <legend className="mb-1.5 font-semibold text-brand-blue">איך תרצו לקבל עדכונים? *</legend>
          <label className="flex items-center gap-2">
            <input type="radio" name="preferred-channel" value="email" checked={preferredChannel === "email"} onChange={() => { setPreferredChannel("email"); setErrors({}); }} required />
            דוא״ל
          </label>
          <label className="flex items-center gap-2">
            <input type="radio" name="preferred-channel" value="whatsapp" checked={preferredChannel === "whatsapp"} onChange={() => { setPreferredChannel("whatsapp"); setErrors({}); }} required />
            וואטסאפ
          </label>
        </fieldset>
      )}
      {(!isProg || phoneRequired) && <div>
        <label htmlFor="phone" className="mb-1.5 block font-semibold text-brand-blue">
          טלפון נייד {phoneRequired ? "*" : <span className="font-normal text-brand-clay">(לא חובה)</span>}
        </label>
        <input
          id="phone"
          type="tel"
          required={phoneRequired}
          dir="ltr"
          inputMode="tel"
          autoComplete="tel"
          maxLength={15}
          className={`${field} text-right`}
          value={values.phone}
          onChange={(e) => setValues({ ...values, phone: e.target.value })}
        />
        {errors.phone && <p className="mt-1 text-sm text-destructive">{errors.phone}</p>}
      </div>}
      {(!isProg || emailRequired) && <div>
        <label htmlFor="email" className="mb-1.5 block font-semibold text-brand-blue">
          דוא״ל {emailRequired ? "*" : <span className="font-normal text-brand-clay">(לא חובה)</span>}
        </label>
        <input
          id="email"
          type="email"
          required={emailRequired}
          dir="ltr"
          autoComplete="email"
          maxLength={255}
          className={`${field} text-right`}
          value={values.email}
          onChange={(e) => setValues({ ...values, email: e.target.value })}
        />
        {errors.email && <p className="mt-1 text-sm text-destructive">{errors.email}</p>}
      </div>}
      <div className="space-y-3">
      <label className="flex cursor-pointer items-start gap-3 text-sm leading-relaxed">
        <input
          type="checkbox"
          required
          className="mt-1 size-5 shrink-0 accent-brand-blue"
          checked={values.consent}
          onChange={(e) => setValues({ ...values, consent: e.target.checked })}
        />
        <span>
          אני מאשר/ת את עיבוד הפרטים שמסרתי (שם, טלפון, דוא״ל) לצורך ההרשמה למפגש, שליחת אישור הרשמה, קישור להתחברות ותזכורות בנוגע למפגש.
        </span>
      </label>
      <label className="flex cursor-pointer items-start gap-3 text-sm leading-relaxed">
        <input
          type="checkbox"
          className="mt-1 size-5 shrink-0 accent-brand-blue"
          checked={values.marketing_consent}
          onChange={(e) => setValues({ ...values, marketing_consent: e.target.checked })}
        />
        <span>
          אני מעוניין/ת לקבל גם תכנים, עדכונים והזמנות נוספות למפגשים/סדנאות במייל ו/או בוואטסאפ מיובל סודאי. ניתן להסיר את עצמי בכל עת.
        </span>
      </label>
      </div>
      {errors.consent && <p className="-mt-3 text-sm text-destructive">{errors.consent}</p>}
      {errors.form && <p className="text-sm text-destructive">{errors.form}</p>}
      <button
        type="submit"
        disabled={status === "sending" || !values.consent}
        className="btn-pill w-full bg-brand-blue text-primary-foreground shadow-soft disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:translate-y-0"
      >
        {status === "sending" ? "שולחים..." : "כן, אני רוצה מקום בשידור החינמי! ←"}
      </button>
    </form>
  );
}
