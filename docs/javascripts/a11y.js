// The theme's search dialog has no accessible name (axe rule aria-dialog-name).
document.querySelectorAll('.md-search[role="dialog"]').forEach((el) => {
  el.setAttribute("aria-label", "Search");
});
