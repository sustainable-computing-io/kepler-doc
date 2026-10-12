// Load the kapa.ai "Ask AI" widget. Configuration reference:
// https://docs.kapa.ai/integrations/website-widget/configuration/behavior
document.addEventListener("DOMContentLoaded", function () {
  var lang = document.documentElement.lang || "en";
  var zh = lang.indexOf("zh") === 0;
  var script = document.createElement("script");
  script.src = "https://widget.kapa.ai/kapa-widget.bundle.js";
  script.async = true;
  script.setAttribute("data-website-id", "d199c53b-6724-4c80-b51c-bb7060e340c7");
  script.setAttribute("data-project-name", "Kepler");
  // Material's teal primary color, same as the header.
  script.setAttribute("data-project-color", "#009485");
  // Material sets the base font size to 20px; kapa assumes 16px.
  script.setAttribute("data-scale-factor", "0.8");
  // No logo: the launcher is a small text button and the modal header shows just the title.
  script.setAttribute("data-modal-logo-hidden", "true");
  script.setAttribute("data-launcher-button-image-width", "0");
  script.setAttribute("data-launcher-button-image-height", "0");
  script.setAttribute("data-launcher-button-font-family", "Roboto, -apple-system, system-ui, Helvetica, Arial, sans-serif");
  script.setAttribute("data-launcher-button-font-size", "14px");
  script.setAttribute("data-launcher-button-font-weight", "500");
  script.setAttribute("data-launcher-button-width", "auto");
  script.setAttribute("data-launcher-button-height", "auto");
  script.setAttribute("data-launcher-button-padding-x", "14px");
  script.setAttribute("data-launcher-button-padding-y", "8px");
  script.setAttribute("data-launcher-button-border-radius", "4px");
  script.setAttribute("data-launcher-button-box-shadow", "0 2px 6px rgba(0, 0, 0, 0.2)");
  script.setAttribute("data-modal-open-on-command-k", "true");
  // Google reCAPTCHA is blocked in mainland China and this site has a zh build.
  script.setAttribute("data-bot-protection-mechanism", "hcaptcha");
  // mkdocs-static-i18n sets <html lang="zh"> on the Chinese build.
  script.setAttribute("data-language", zh ? "zh" : "en");
  // The widget translates its own UI but not these, so give the zh build its own set.
  script.setAttribute(
    "data-example-questions",
    zh
      ? "如何使用 Helm 安装 Kepler？," +
        "为什么我的节点上 RAPL 不可用？," +
        "功耗是如何分配到容器的？"
      : "How do I install Kepler with Helm?," +
        "Why is RAPL unavailable on my node?," +
        "How is power attributed to containers?"
  );
  // The site has no cookie consent banner, so do not set kapa's anonymous tracking cookie.
  script.setAttribute("data-user-analytics-cookie-enabled", "false");
  document.head.appendChild(script);
});
