import { mkdir, readFile, writeFile } from "node:fs/promises";

const channels = JSON.parse(await readFile("channels.json", "utf8"));
const template = await readFile("dist/index.html", "utf8");
for (const source of channels) {
  const channelDir = "dist/" + source;
  await mkdir(channelDir + "/thank-you", { recursive: true });
  const landing = template.replace('id="root"', 'id="root" data-source="' + source + '"');
  const landingWithScroll = source === "hitdabrut"
    ? landing.replace("</head>", [
      '  <link rel="stylesheet" href="/merivah-lekirva-webinar/hitdabrut-scroll.css?v=5">',
      "</head>",
    ].join("\n"))
    : landing;
  await writeFile(channelDir + "/index.html", landingWithScroll);
  const thanks = landing.replace('id="root"', 'id="root" data-page="thanks"')
    .replace(/<title>.*?<\/title>/, "<title>תודה שנרשמתם — ממריבה לקרבה</title>");
  await writeFile(channelDir + "/thank-you/index.html", thanks);
}

await mkdir("dist/quiz", { recursive: true });
const quizPage = template.replace('id="root"', 'id="root" data-page="quiz"')
  .replace(/<title>.*?<\/title>/, "<title>איפה הזוגיות שלכם ממש עומדת? — שאלון עם יובל סודאי</title>");
await writeFile("dist/quiz/index.html", quizPage);

const links = channels.map(source => '<li><a href="./' + source + '/" dir="ltr">' + source + '</a></li>').join("\n")
  + '\n<li><a href="./quiz/" dir="ltr">quiz (שאלון זוגיות)</a></li>';
const directory = template.replace(/<script type="module"[^>]*><\/script>/g, "")
  .replace('<div id="root"></div>', '<main><h1>ממריבה לקרבה — קישורים לפי ערוץ</h1><ul>' + links + '</ul></main>')
  .replace(/<noscript>.*?<\/noscript>/, "");
await writeFile("dist/index.html", directory);
await writeFile("dist/.nojekyll", "");

const aliases = {"nava": "influencer-nava", "yuval": "email-yuval-internal", "shvirega": "influencer-shevi", "status": "whatsapp-status", "group": "whatsapp-group", "personal": "personal-circles"};
for (const [alias, canonical] of Object.entries(aliases)) {
  await mkdir("dist/" + alias + "/thank-you", {recursive:true});
  await writeFile("dist/" + alias + "/index.html", await readFile("dist/" + canonical + "/index.html", "utf8"));
  await writeFile("dist/" + alias + "/thank-you/index.html", await readFile("dist/" + canonical + "/thank-you/index.html", "utf8"));
}
