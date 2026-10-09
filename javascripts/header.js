// Show the navigation tabs in the header row, next to the logo and site name
const tabs = document.querySelector(".md-tabs");
const title = document.querySelector(".md-header__title");
if (tabs && title) {
  title.after(tabs);
}

// Link the site name to the home page, like the logo
const logo = document.querySelector(".md-header__button.md-logo");
const name = document.querySelector(".md-header__topic:first-child .md-ellipsis");
if (logo && name) {
  const link = document.createElement("a");
  link.href = logo.href;
  link.className = "md-header__home";
  link.textContent = name.textContent.trim();
  name.replaceChildren(link);
}
