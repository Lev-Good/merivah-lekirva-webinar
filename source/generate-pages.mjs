import { mkdir, readFile, writeFile } from "node:fs/promises";

const channels = JSON.parse(await readFile("channels.json", "utf8"));
const template = await readFile("dist/index.html", "utf8");
for (const source of channels) {
  const channelDir = "dist/" + source;
  await mkdir(channelDir + "/thank-you", { recursive: true });
  const landing = template.replace('id="root"', 'id="root" data-source="' + source + '"');
  const landingWithScroll = source === "hitdabrut"
    ? landing.replace("</head>", [
      '  <link rel="stylesheet" href="/merivah-lekirva-webinar/hitdabrut-scroll.css?v=3">',
      '  <script type="module" src="/merivah-lekirva-webinar/hitdabrut-scroll.js?v=2"></script>',
      "</head>",
    ].join("\n"))
    : landing;
  await writeFile(channelDir + "/index.html", landingWithScroll);
  const thanks = landing.replace('id="root"', 'id="root" data-page="thanks"')
    .replace(/<title>.*?<\/title>/, "<title>תודה שנרשמתם — ממריבה לקרבה</title>");
  await writeFile(channelDir + "/thank-you/index.html", thanks);
}

const links = channels.map(source => '<li><a href="./' + source + '/" dir="ltr">' + source + '</a></li>').join("\n");
const directory = template.replace(/<script type="module"[^>]*><\/script>/g, "")
  .replace('<div id="root"></div>', '<main><h1>ממריבה לקרבה — קישורים לפי ערוץ</h1><ul>' + links + '</ul></main>')
  .replace(/<noscript>.*?<\/noscript>/, "");
await writeFile("dist/index.html", directory);
await writeFile("dist/.nojekyll", "");
