import { createRoot } from "react-dom/client";
import { Index } from "./routes/index";
import { ThankYou } from "./routes/thank-you";
import { Quiz } from "./routes/quiz";
import "./styles.css";

const root = document.getElementById("root")!;
const page = root.dataset.page;
createRoot(root).render(
  page === "thanks" ? <ThankYou /> : page === "quiz" ? <Quiz /> : <Index source={root.dataset.source ?? ""} />
);
