(function () {
  let currentPage = 0;
  const pageImage = document.getElementById("pageImage");
  const pageIndicator = document.getElementById("pageIndicator");
  const headerPageIndicator = document.getElementById("headerPageIndicator");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const shareWhatsApp = document.getElementById("shareWhatsApp");
  const shareEmail = document.getElementById("shareEmail");
  const shareDropdown = document.getElementById("shareDropdown");
  const shareTrigger = document.getElementById("shareTrigger");
  const listenDropdown = document.getElementById("listenDropdown");
  const listenTrigger = document.getElementById("listenTrigger");

  function pageUrl(index) {
    return "/book/" + bookId + "/pages/" + pages[index];
  }

  function updatePage() {
    if (pages.length === 0) return;
    pageImage.src = pageUrl(currentPage);
    pageImage.alt = "Page " + (currentPage + 1);
    const text = (currentPage + 1) + " / " + pages.length;
    pageIndicator.textContent = text;
    if (headerPageIndicator) headerPageIndicator.textContent = text;
    prevBtn.disabled = currentPage <= 0;
    nextBtn.disabled = currentPage >= pages.length - 1;
    const headerPrev = document.getElementById("headerPrevBtn");
    const headerNext = document.getElementById("headerNextBtn");
    const undoBtnEl = document.getElementById("undoBtn");
    const redoBtnEl = document.getElementById("redoBtn");
    if (headerPrev) headerPrev.disabled = currentPage <= 0;
    if (headerNext) headerNext.disabled = currentPage >= pages.length - 1;
    if (undoBtnEl) undoBtnEl.disabled = currentPage <= 0;
    if (redoBtnEl) redoBtnEl.disabled = currentPage >= pages.length - 1;
  }

  function goPrev() {
    if (currentPage > 0) {
      currentPage--;
      updatePage();
    }
  }

  function goNext() {
    if (currentPage < pages.length - 1) {
      currentPage++;
      updatePage();
    }
  }

  prevBtn.addEventListener("click", goPrev);
  nextBtn.addEventListener("click", goNext);

  const undoBtn = document.getElementById("undoBtn");
  const redoBtn = document.getElementById("redoBtn");
  const headerPrevBtn = document.getElementById("headerPrevBtn");
  const headerNextBtn = document.getElementById("headerNextBtn");
  if (undoBtn) undoBtn.addEventListener("click", goPrev);
  if (redoBtn) redoBtn.addEventListener("click", goNext);
  if (headerPrevBtn) headerPrevBtn.addEventListener("click", goPrev);
  if (headerNextBtn) headerNextBtn.addEventListener("click", goNext);

  // Touch swipe (optional)
  let touchStartX = 0;
  document.querySelector(".page-area").addEventListener("touchstart", function (e) {
    touchStartX = e.touches[0].clientX;
  }, { passive: true });
  document.querySelector(".page-area").addEventListener("touchend", function (e) {
    var dx = e.changedTouches[0].clientX - touchStartX;
    if (dx > 60) goPrev();
    else if (dx < -60) goNext();
  }, { passive: true });

  // Share links
  const bookTitleText = typeof bookTitle === "string" ? bookTitle : (document.getElementById("storybookTitle") && document.getElementById("storybookTitle").textContent) || "Story book";
  shareWhatsApp.href =
    "https://wa.me/?text=" + encodeURIComponent(bookUrl);
  shareEmail.href =
    "mailto:?subject=" + encodeURIComponent("Story book: " + bookTitleText) +
    "&body=" + encodeURIComponent("Read this book: " + bookUrl);

  // Share dropdown
  function closeAllDropdowns() {
    shareDropdown.hidden = true;
    if (shareTrigger) shareTrigger.setAttribute("aria-expanded", "false");
    listenDropdown.hidden = true;
    if (listenTrigger) listenTrigger.setAttribute("aria-expanded", "false");
  }

  if (shareTrigger && shareDropdown) {
    shareTrigger.addEventListener("click", function (e) {
      e.stopPropagation();
      const open = !shareDropdown.hidden;
      closeAllDropdowns();
      if (!open) {
        shareDropdown.hidden = false;
        shareTrigger.setAttribute("aria-expanded", "true");
      }
    });
    shareDropdown.addEventListener("click", function (e) { e.stopPropagation(); });
  }

  document.getElementById("shareCopyLink").addEventListener("click", function () {
    navigator.clipboard.writeText(bookUrl).then(function () {
      closeAllDropdowns();
    });
  });

  document.addEventListener("click", closeAllDropdowns);

  // Listen dropdown and TTS
  if (listenTrigger && listenDropdown) {
    listenTrigger.addEventListener("click", function (e) {
      e.stopPropagation();
      const open = !listenDropdown.hidden;
      closeAllDropdowns();
      if (!open) {
        listenDropdown.hidden = false;
        listenTrigger.setAttribute("aria-expanded", "true");
      }
    });
    listenDropdown.addEventListener("click", function (e) { e.stopPropagation(); });
  }

  let speechUtterance = null;
  const listenStartBtn = document.getElementById("listenStart");
  const listenStopBtn = document.getElementById("listenStop");

  // Prefer a voice that sounds like a young Indian girl: en-IN, female, then use higher pitch.
  function getYoungIndianVoice() {
    const voices = window.speechSynthesis.getVoices();
    if (!voices.length) return null;
    var lower = function (s) { return (s || "").toLowerCase(); };
    // Prefer Indian English female (e.g. Veena, Lekha on Windows)
    var best = voices.find(function (v) {
      return (v.lang === "en-IN" || v.lang === "hi-IN") && (lower(v.name).indexOf("female") !== -1 || lower(v.name).indexOf("woman") !== -1 || v.name.indexOf("Veena") !== -1 || v.name.indexOf("Lekha") !== -1);
    });
    if (best) return best;
    // Any Indian English
    best = voices.find(function (v) { return v.lang === "en-IN" || v.lang === "hi-IN"; });
    if (best) return best;
    // Fallback: English female for similar clarity
    best = voices.find(function (v) {
      return v.lang.startsWith("en") && (lower(v.name).indexOf("female") !== -1 || lower(v.name).indexOf("woman") !== -1 || lower(v.name).indexOf("zira") !== -1 || lower(v.name).indexOf("samantha") !== -1);
    });
    return best || null;
  }

  // Voices load async in many browsers; ensure we have a list when user clicks.
  if (window.speechSynthesis) {
    window.speechSynthesis.getVoices();
    window.speechSynthesis.onvoiceschanged = function () { window.speechSynthesis.getVoices(); };
  }

  if (listenStartBtn) {
    listenStartBtn.addEventListener("click", function () {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
        const pageText = (typeof pageTexts !== "undefined" && pageTexts[currentPage]) ? pageTexts[currentPage].trim() : "";
        const text = pageText
          ? bookTitleText + ". Page " + (currentPage + 1) + ". " + pageText
          : bookTitleText + ". Page " + (currentPage + 1) + " of " + pages.length + ".";
        speechUtterance = new SpeechSynthesisUtterance(text);
        speechUtterance.rate = 0.9;
        speechUtterance.pitch = 1.2;
        var chosen = getYoungIndianVoice();
        if (chosen) speechUtterance.voice = chosen;
        window.speechSynthesis.speak(speechUtterance);
        closeAllDropdowns();
      }
    });
  }

  if (listenStopBtn) {
    listenStopBtn.addEventListener("click", function () {
      if (window.speechSynthesis) window.speechSynthesis.cancel();
      closeAllDropdowns();
    });
  }

  // Print
  document.getElementById("printBtn").addEventListener("click", function () {
    window.print();
  });

  // Invite a friend: open share dropdown (or copy link)
  const inviteBtn = document.getElementById("inviteBtn");
  if (inviteBtn) {
    inviteBtn.addEventListener("click", function (e) {
      e.preventDefault();
      closeAllDropdowns();
      listenDropdown.hidden = true;
      shareDropdown.hidden = false;
      if (shareTrigger) shareTrigger.setAttribute("aria-expanded", "true");
    });
  }

  updatePage();
})();
