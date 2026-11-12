import { createRoot } from "react-dom/client";
import { Index } from "./routes/index";
import { ThankYou } from "./routes/thank-you";
import "./styles.css";

const root = document.getElementById("root")!;
createRoot(root).render(root.dataset.page === "thanks" ? <ThankYou /> : <Index source={root.dataset.source ?? ""} />);
