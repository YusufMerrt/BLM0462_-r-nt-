/**
 * BLM0462 Vize Quiz — tek soru modu, anında doğru/yanlış
 */
(function () {
  function letterFor(i) {
    return String.fromCharCode(65 + i);
  }

  function normalizeANS(s) {
    if (s == null) return "";
    return String(s)
      .toLocaleLowerCase("tr-TR")
      .trim()
      .replace(/\s+/g, " ")
      .replace(/[.,;:!?]+$/g, "");
  }

  function fibMatches(userRaw, expectedRaw) {
    const u = normalizeANS(userRaw);
    if (!expectedRaw) return !u;
    const exp = String(expectedRaw).trim();
    const variants = [];

    function addVariant(v) {
      const n = normalizeANS(v);
      if (n) variants.push(n);
      const noParen = n.replace(/\s*\([^)]*\)/g, "").trim();
      if (noParen && noParen !== n) variants.push(noParen);
    }

    addVariant(exp);

    if (/\s\/\s/.test(exp)) {
      exp.split(/\s*\/\s*/).forEach((p) => addVariant(p.trim()));
    } else if (exp.includes("/")) {
      exp.split("/").forEach((p) => addVariant(p.trim()));
    }

    if (exp.includes(" veya ")) {
      exp.split(" veya ").forEach((p) => addVariant(p.trim()));
    }

    const uniq = [...new Set(variants)];
    return uniq.some((v) => u === v);
  }

  let data = null;
  let queue = [];
  let currentIndex = 0;
  let filter = "all";
  let topicFilter = "all";
  /**
   * @type Map<string, {
   *   revealed: boolean,
   *   mcqIndex?: number,
   *   fibValues?: string[],
   * }>
   */
  const memory = new Map();

  function tfToMcqShape(q) {
    return {
      id: q.id,
      topic: q.topic,
      question: q.statement,
      options: ["Doğru", "Yanlış"],
      correctIndex: q.correctTrue ? 0 : 1,
      explanation: q.explanation || "",
      _plainText: true,
    };
  }

  const els = {
    title: document.getElementById("app-title"),
    subtitle: document.getElementById("app-subtitle"),
    main: document.getElementById("quiz-main"),
    progress: document.getElementById("progress"),
    btnReset: document.getElementById("btn-reset"),
    topicSelect: document.getElementById("topic-filter"),
  };

  function getKey(item) {
    return `${item.type}-${item.data.id}`;
  }

  function buildQueue() {
    const mcq = data.mcq.map((q) => ({ type: "mcq", data: q }));
    const fib = data.fib.map((q) => ({ type: "fib", data: q }));
    const tf = (data.tf || []).map((q) => ({ type: "tf", data: q }));
    let items;
    if (filter === "mcq") items = mcq;
    else if (filter === "fib") items = fib;
    else if (filter === "tf") items = tf;
    else items = [...mcq, ...fib, ...tf];
    if (topicFilter !== "all") {
      items = items.filter((it) => (it.data.topic || "") === topicFilter);
    }
    return items;
  }

  function topicLabel(slug) {
    if (!slug || !data.topics) return "";
    const t = data.topics.find((x) => x.id === slug);
    return t ? t.label : slug;
  }

  function loadData() {
    if (window.QUIZ_DATA) {
      data = window.QUIZ_DATA;
      return Promise.resolve();
    }
    return fetch("questions.json")
      .then((r) => r.json())
      .then((j) => {
        data = j;
      });
  }

  function splitFibSentence(sentence) {
    return { parts: sentence.split(/_{3,}/g) };
  }

  function renderMcqCard(q, mem) {
    const id = `mcq-${q.id}-${currentIndex}`;
    const card = document.createElement("article");
    card.className = "card card-single";

    const h = document.createElement("h3");
    h.textContent =
      q._tfKind === "dy"
        ? `Doğru / Yanlış · Soru ${q.id}`
        : `Çoktan seçmeli · Soru ${q.id}`;
    card.appendChild(h);
    if (q.topic) {
      const tag = document.createElement("p");
      tag.className = "topic-tag";
      tag.textContent = topicLabel(q.topic);
      card.appendChild(tag);
    }

    const p = document.createElement("p");
    p.className = "q-text";
    if (q._plainText) p.textContent = q.question;
    else p.innerHTML = q.question;
    card.appendChild(p);

    const opts = document.createElement("div");
    opts.className =
      q._tfKind === "dy" ? "options options-tf" : "options";

    const nOpt = q.options.length;
    q.options.forEach((opt, i) => {
      const label = document.createElement("label");
      label.className = "option";
      label.dataset.index = String(i);

      const input = document.createElement("input");
      input.type = "radio";
      input.name = id;
      input.value = String(i);
      if (mem && mem.mcqIndex === i) input.checked = true;

      const spanL = document.createElement("span");
      spanL.className = "label";
      spanL.textContent =
        nOpt <= 5 ? `${letterFor(i)})` : `${i + 1})`;

      const spanT = document.createElement("span");
      spanT.className = "text";
      spanT.textContent = opt;

      label.appendChild(input);
      label.appendChild(spanL);
      label.appendChild(spanT);
      opts.appendChild(label);
    });

    card.appendChild(opts);
    return card;
  }

  function renderFibCard(q, mem) {
    const card = document.createElement("article");
    card.className = "card card-single";

    const h = document.createElement("h3");
    h.textContent = `Boşluk doldurma · Soru ${q.id}`;
    card.appendChild(h);
    if (q.topic) {
      const tag = document.createElement("p");
      tag.className = "topic-tag";
      tag.textContent = topicLabel(q.topic);
      card.appendChild(tag);
    }

    const { parts } = splitFibSentence(q.sentence);
    const nFromUnderscore = Math.max(0, parts.length - 1);
    const nBlanks =
      q.answers && q.answers.length ? q.answers.length : nFromUnderscore;

    const line = document.createElement("div");
    line.className = "fib-line";

    const saved = (mem && mem.fibValues) || [];

    for (let i = 0; i < nBlanks; i++) {
      if (parts[i] != null) {
        const span = document.createElement("span");
        span.textContent = parts[i];
        line.appendChild(span);
      }
      const inp = document.createElement("input");
      inp.type = "text";
      inp.className = "fib-input";
      inp.autocomplete = "off";
      inp.placeholder = `Boşluk ${i + 1}`;
      inp.dataset.blankIndex = String(i);
      if (saved[i] != null) inp.value = saved[i];
      line.appendChild(inp);
    }
    if (parts[nBlanks] != null) {
      const span = document.createElement("span");
      span.textContent = parts[nBlanks];
      line.appendChild(span);
    }

    card.appendChild(line);
    return card;
  }

  function applyMcqReveal(card, q) {
    card.classList.add("checked");
    const sel = card.querySelector('input[type="radio"]:checked');
    const idx = sel ? parseInt(sel.value, 10) : -1;

    card.querySelectorAll(".option").forEach((lab) => {
      lab.classList.remove("selected", "correct", "wrong", "correct-answer");
      const i = parseInt(lab.dataset.index, 10);
      const input = lab.querySelector("input");
      if (input.checked) lab.classList.add("selected");
      if (i === q.correctIndex) lab.classList.add("correct-answer");
      if (input.checked && i === q.correctIndex) lab.classList.add("correct");
      if (input.checked && i !== q.correctIndex) lab.classList.add("wrong");
    });
    return idx;
  }

  function applyFibReveal(card, q) {
    card.classList.add("checked");
    const inputs = [...card.querySelectorAll(".fib-input")];
    inputs.forEach((inp, i) => {
      inp.classList.remove("correct", "wrong");
      const expected = q.answers[i] || "";
      const ok = fibMatches(inp.value, expected);
      inp.classList.add(ok ? "correct" : "wrong");
    });
    return inputs;
  }

  function getMcqCorrectText(q) {
    const i = q.correctIndex;
    const pref =
      q.options.length <= 5 ? letterFor(i) : String(i + 1);
    return `${pref}) ${q.options[i]}`;
  }

  function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function fillFeedbackPanel(feedbackEl, ok, item) {
    feedbackEl.classList.remove("hidden", "feedback-ok", "feedback-bad");
    feedbackEl.classList.add(ok ? "feedback-ok" : "feedback-bad");

    if (item.type === "mcq" || item.type === "tf") {
      const q =
        item.type === "tf" ? tfToMcqShape(item.data) : item.data;
      if (ok) {
        feedbackEl.innerHTML =
          '<p class="feedback-title">Doğru!</p>' +
          (q.explanation
            ? `<p class="feedback-note">${escapeHtml(q.explanation)}</p>`
            : "");
      } else {
        feedbackEl.innerHTML =
          '<p class="feedback-title">Yanlış</p>' +
          `<p class="feedback-correct">Doğru cevap: <strong>${escapeHtml(
            getMcqCorrectText(q)
          )}</strong></p>` +
          (q.explanation
            ? `<p class="feedback-note">${escapeHtml(q.explanation)}</p>`
            : "");
      }
      return;
    }

    const q = item.data;
    if (ok) {
      feedbackEl.innerHTML =
        '<p class="feedback-title">Doğru!</p>' +
        (q.explanation
          ? `<p class="feedback-note">${escapeHtml(q.explanation)}</p>`
          : "");
    } else {
      const lines = q.answers.map(
        (a, i) =>
          `<li><strong>Boşluk ${i + 1}:</strong> ${escapeHtml(a)}</li>`
      );
      feedbackEl.innerHTML =
        '<p class="feedback-title">Yanlış veya eksik</p>' +
        '<p class="feedback-correct-label">Doğru cevaplar:</p>' +
        `<ul class="feedback-list">${lines.join("")}</ul>` +
        (q.explanation
          ? `<p class="feedback-note">${escapeHtml(q.explanation)}</p>`
          : "");
    }
  }

  function saveDraft(item) {
    const key = getKey(item);
    const existing = memory.get(key);
    if (existing && existing.revealed) return;

    if (item.type === "mcq" || item.type === "tf") {
      const sel = els.main.querySelector('.card input[type="radio"]:checked');
      if (sel) {
        memory.set(key, {
          revealed: false,
          mcqIndex: parseInt(sel.value, 10),
        });
      }
    } else {
      const inputs = [
        ...els.main.querySelectorAll(".fib-input"),
      ].map((inp) => inp.value);
      if (inputs.length) {
        memory.set(key, { revealed: false, fibValues: inputs });
      }
    }
  }

  function evaluateCurrent(item, card, feedbackEl, btnCheck, btnNext) {
    const key = getKey(item);

    if (item.type === "mcq") {
      const sel = card.querySelector('input[type="radio"]:checked');
      if (!sel) {
        alert("Lütfen bir şık seçin.");
        return;
      }
      const idx = parseInt(sel.value, 10);
      memory.set(key, { revealed: true, mcqIndex: idx });
      applyMcqReveal(card, item.data);
      const ok = idx === item.data.correctIndex;
      fillFeedbackPanel(feedbackEl, ok, item);
      btnCheck.disabled = true;
      btnNext.disabled = false;
      return;
    }

    if (item.type === "tf") {
      const sel = card.querySelector('input[type="radio"]:checked');
      if (!sel) {
        alert("Lütfen Doğru veya Yanlış seçin.");
        return;
      }
      const idx = parseInt(sel.value, 10);
      const m = tfToMcqShape(item.data);
      memory.set(key, { revealed: true, mcqIndex: idx });
      applyMcqReveal(card, m);
      const ok = idx === m.correctIndex;
      fillFeedbackPanel(feedbackEl, ok, { type: "tf", data: item.data });
      btnCheck.disabled = true;
      btnNext.disabled = false;
      return;
    }

    const inputs = [...card.querySelectorAll(".fib-input")];
    if (!inputs.length) return;
    const vals = inputs.map((inp) => inp.value);
    if (vals.some((v) => normalizeANS(v) === "")) {
      alert("Lütfen tüm boşlukları doldurun.");
      return;
    }

    memory.set(key, { revealed: true, fibValues: vals });
    applyFibReveal(card, item.data);
    const allOk = inputs.every((inp, i) =>
      fibMatches(inp.value, item.data.answers[i] || "")
    );
    fillFeedbackPanel(feedbackEl, allOk, item);
    btnCheck.disabled = true;
    btnNext.disabled = false;
  }

  function renderCurrent() {
    els.main.innerHTML = "";

    if (!queue.length) {
      els.main.innerHTML =
        '<p class="empty-msg">Bu filtrede soru yok.</p>';
      els.progress.textContent = "—";
      return;
    }

    if (currentIndex >= queue.length) currentIndex = queue.length - 1;
    if (currentIndex < 0) currentIndex = 0;

    const item = queue[currentIndex];
    const key = getKey(item);
    const mem = memory.get(key);

    els.progress.textContent = `Soru ${currentIndex + 1} / ${queue.length}`;

    const wrap = document.createElement("div");
    wrap.className = "single-wrap";

    let card;
    if (item.type === "mcq") {
      card = renderMcqCard(item.data, mem);
    } else if (item.type === "tf") {
      const wrapped = tfToMcqShape(item.data);
      wrapped._tfKind = "dy";
      card = renderMcqCard(wrapped, mem);
    } else {
      card = renderFibCard(item.data, mem);
    }

    const feedback = document.createElement("div");
    feedback.id = "feedback-panel";
    feedback.className = "feedback-panel hidden";

    const nav = document.createElement("div");
    nav.className = "nav-row";

    const btnPrev = document.createElement("button");
    btnPrev.type = "button";
    btnPrev.className = "btn-nav btn-prev";
    btnPrev.textContent = "← Önceki";
    btnPrev.disabled = currentIndex === 0;

    const btnCheck = document.createElement("button");
    btnCheck.type = "button";
    btnCheck.className = "btn-nav btn-check";
    btnCheck.textContent = "Cevabı kontrol et";

    const btnNext = document.createElement("button");
    btnNext.type = "button";
    btnNext.className = "btn-nav btn-next";
    const isLast = currentIndex >= queue.length - 1;
    btnNext.textContent = isLast ? "Tamam" : "Sonraki soru →";

    wrap.appendChild(card);
    wrap.appendChild(feedback);
    nav.appendChild(btnPrev);
    nav.appendChild(btnCheck);
    nav.appendChild(btnNext);
    wrap.appendChild(nav);
    els.main.appendChild(wrap);

    const revealed = mem && mem.revealed;
    if (revealed) {
      if (item.type === "mcq") {
        applyMcqReveal(card, item.data);
        const ok = mem.mcqIndex === item.data.correctIndex;
        fillFeedbackPanel(feedback, ok, item);
      } else if (item.type === "tf") {
        const m = tfToMcqShape(item.data);
        applyMcqReveal(card, m);
        const ok = mem.mcqIndex === m.correctIndex;
        fillFeedbackPanel(feedback, ok, { type: "tf", data: item.data });
      } else {
        applyFibReveal(card, item.data);
        const inputs = [...card.querySelectorAll(".fib-input")];
        const allOk = inputs.every((inp, i) =>
          fibMatches(inp.value, item.data.answers[i] || "")
        );
        fillFeedbackPanel(feedback, allOk, item);
      }
      feedback.classList.remove("hidden");
      btnCheck.disabled = true;
      btnNext.disabled = false;
    } else {
      btnCheck.disabled = false;
      btnNext.disabled = true;
    }

    btnPrev.addEventListener("click", () => {
      saveDraft(item);
      currentIndex--;
      renderCurrent();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    btnCheck.addEventListener("click", () => {
      evaluateCurrent(item, card, feedback, btnCheck, btnNext);
      feedback.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });

    btnNext.addEventListener("click", () => {
      const done = memory.get(key)?.revealed;
      if (!done) {
        alert('Önce "Cevabı kontrol et" ile cevabınızı gönderin.');
        return;
      }
      saveDraft(item);
      if (isLast) {
        feedback.classList.remove("hidden", "feedback-bad");
        feedback.classList.add("feedback-ok");
        feedback.innerHTML =
          '<p class="feedback-title">Bu sette son soruya ulaştınız.</p>' +
          '<p class="feedback-note">Filtreyi değiştirebilir veya Sıfırla ile baştan başlayabilirsiniz.</p>';
        btnNext.disabled = true;
        return;
      }
      currentIndex++;
      renderCurrent();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  function applyFilter(btn) {
    document.querySelectorAll("[data-filter]").forEach((b) =>
      b.classList.remove("active")
    );
    btn.classList.add("active");
    filter = btn.dataset.filter;
    queue = buildQueue();
    currentIndex = 0;
    renderCurrent();
  }

  function applyTopicFilter() {
    if (!els.topicSelect) return;
    topicFilter = els.topicSelect.value || "all";
    queue = buildQueue();
    currentIndex = 0;
    renderCurrent();
  }

  function fillTopicOptions() {
    if (!els.topicSelect || !data.topics) return;
    const sel = els.topicSelect;
    sel.innerHTML = "";
    const o0 = document.createElement("option");
    o0.value = "all";
    o0.textContent = "Tüm konular";
    sel.appendChild(o0);
    data.topics.forEach((t) => {
      const o = document.createElement("option");
      o.value = t.id;
      o.textContent = t.label;
      sel.appendChild(o);
    });
    if ([...sel.options].some((o) => o.value === topicFilter)) {
      sel.value = topicFilter;
    } else {
      topicFilter = "all";
      sel.value = "all";
    }
  }

  function resetAll() {
    memory.clear();
    currentIndex = 0;
    queue = buildQueue();
    renderCurrent();
  }

  function initToolbar() {
    document.querySelectorAll("[data-filter]").forEach((btn) => {
      btn.addEventListener("click", () => applyFilter(btn));
    });
    if (els.topicSelect) {
      els.topicSelect.addEventListener("change", () => applyTopicFilter());
    }
    els.btnReset.addEventListener("click", () => {
      if (confirm("Tüm cevaplar ve ilerleme sıfırlansın mı?")) resetAll();
    });
  }

  function build() {
    els.title.textContent = data.title;
    els.subtitle.textContent =
      (data.subtitle || "") +
      " — Tek tek soru; kontrol edince doğru/yanlış ve doğru cevap gösterilir.";

    queue = buildQueue();
    fillTopicOptions();
    initToolbar();
    renderCurrent();
  }

  loadData()
    .then(() => build())
    .catch((err) => {
      els.main.innerHTML =
        '<p class="empty-msg">Veri yüklenemedi. <code>questions-data.js</code> dosyası gerekli.</p>';
      console.error(err);
    });
})();
