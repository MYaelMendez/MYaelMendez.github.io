// PC:// · omnibox: type "pc" + space + an address (wilhælm.t, æ://llm.store/hermes, hermes@llm.store)
const open = (q) => chrome.tabs.create({ url: chrome.runtime.getURL("index.html?q=" + encodeURIComponent(q)) });
chrome.omnibox.setDefaultSuggestion({ description: "Resolve with PC:// (æQR ↔ email): %s" });
chrome.omnibox.onInputEntered.addListener((text) => open(text.trim()));
// Side panel where supported (Chrome, Edge, Brave). Opera falls back to the popup.
if (chrome.sidePanel && chrome.sidePanel.setPanelBehavior) {
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: false }).catch(() => {});
}
