import { Flower } from "@/components/landing/Flower";
import { Button } from "@/components/ui/button";


const ZOOM_REGISTER_URL = "https://us06web.zoom.us/webinar/register/WN_yGDggiizS7S9jJhc3S7GwA";
const WHATSAPP_URL = "https://chat.whatsapp.com/Kh9aZcX6IkRE6XYOl8tFf4?s=cl&p=a&iam=2";


export function ThankYou() {
  return (
    <main className="flex min-h-svh flex-col bg-background">
      <header className="border-b border-border px-6 py-5">
        <a href="../" className="mx-auto flex max-w-6xl items-center gap-2 font-bold text-brand-blue">
          <Flower size={32} />
          יובל סודאי
        </a>
      </header>
      <section className="mx-auto flex w-full max-w-3xl flex-1 flex-col items-center justify-center px-5 py-16 text-center sm:py-24">
        <Flower size={80} className="mb-6" />
        <h1 className="font-display-tight text-5xl sm:text-7xl">איזה יופי שנרשמתם! 🎉</h1>
        <p className="mt-6 max-w-xl text-lg leading-relaxed sm:text-xl">
          קיבלנו את הפרטים שלכם. לחצו למטה כדי להשלים את ההרשמה בזום. אפשר גם להצטרף לקבוצת הוואטסאפ שלנו.
        </p>
        <ul className="mt-8 flex flex-wrap justify-center gap-2.5 text-[0.95rem] font-semibold">
          {["📅 יום רביעי | 18.11.2026 (ח׳ כסלו)", "🕣 בשעה 20:30", "💻 בזום, מהבית"].map((detail) => (
            <li key={detail} className="rounded-full border border-border bg-card px-4 py-2 text-brand-blue shadow-soft">
              {detail}
            </li>
          ))}
        </ul>
        <p className="mt-10 max-w-xl text-base font-semibold leading-relaxed text-brand-blue sm:text-lg">
          עוד צעד קטן אחד: השלימו הרשמה קצרה אצל זום (שם ומייל) ותקבלו מיד את קישור הכניסה האישי שלכם למפגש.
        </p>
        <Button asChild className="btn-pill mt-4 h-auto max-w-full whitespace-normal bg-brand-blue px-10 py-5 text-lg text-primary-foreground shadow-card hover:bg-brand-blue-deep">
          <a href={ZOOM_REGISTER_URL} target="_blank" rel="noopener noreferrer">
            להשלמת ההרשמה וקבלת קישור כניסה אישי ←
          </a>
        </Button>
        <Button asChild className="btn-pill mt-4 h-auto max-w-full whitespace-normal bg-brand-pink text-brand-blue shadow-soft hover:bg-brand-pink hover:shadow-card">
          <a href={WHATSAPP_URL} target="_blank" rel="noopener noreferrer">
            הצטרפו לקבוצת הוואטסאפ שלנו ←
          </a>
        </Button>
        <Button asChild variant="link" className="mt-5 h-auto text-base text-brand-blue">
          <a href="../">חזרה לעמוד הראשי</a>
        </Button>
      </section>
    </main>
  );
}
