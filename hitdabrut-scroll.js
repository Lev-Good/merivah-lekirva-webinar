const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
const sectionSelector = '#root[data-source="hitdabrut"] > div > section:not(#register)';
const resistanceRange = 68;
const resistance = 0.48;

window.addEventListener("wheel", (event) => {
  if (!event.cancelable || event.defaultPrevented || event.ctrlKey || event.shiftKey
      || reducedMotion.matches || event.deltaMode === WheelEvent.DOM_DELTA_PAGE
      || event.deltaY <= 0 || Math.abs(event.deltaX) >= event.deltaY) return;

  const delta = event.deltaY * (event.deltaMode === WheelEvent.DOM_DELTA_LINE ? 16 : 1);
  const marker = innerHeight * 0.65;
  const boundary = Array.from(document.querySelectorAll(sectionSelector))
    .map(section => section.getBoundingClientRect().top - marker)
    .find(distance => distance > -resistanceRange && distance <= delta);
  if (boundary === undefined) return;

  const before = Math.max(0, boundary);
  const remaining = delta - before;
  const distanceInRange = Math.max(0, resistanceRange + Math.min(0, boundary));
  const slowed = Math.min(remaining, distanceInRange / resistance);
  const movement = before + slowed * resistance + (remaining - slowed);
  if (movement >= delta) return;

  event.preventDefault();
  window.scrollBy({ top: Math.max(1, movement), behavior: "instant" });
}, { passive: false });
