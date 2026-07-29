/* ============================================================
   body-interactions.js
   正文互動層：打字機效果
   ============================================================ */
(function () {
  "use strict";

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  /* ---------------------------------------------------------
     Typewriter — 用 requestAnimationFrame 依「已過時間比例」
     直接算出該顯示幾個字，不受 setTimeout 最小延遲（瀏覽器約 4ms
     下限）限制，才能真正做到「整行在極短時間內打完」。
  --------------------------------------------------------- */
  var LINE_DURATION_MS = 1500; // 每一行／每個 segment 的目標完成時間（約1.5秒）
  var LINE_GAP_MS = 220;       // 多行段落之間的停頓

  function isCommaPause(ch) {
    return /[，、；]/.test(ch);
  }
  function isEndPause(ch) {
    return /[。？！」]/.test(ch);
  }
  function charWeight(ch) {
    if (isEndPause(ch)) return 2.4;
    if (isCommaPause(ch)) return 1.7;
    return 1;
  }

  // 以 rAF 依累積權重比例逐字顯示，讓標點仍保有些微停頓感，
  // 但整體一定會在 duration 時間內顯示完畢。
  function typeInto(target, text, duration, onDone) {
    var length = text.length;
    if (!length) {
      if (onDone) onDone();
      return;
    }
    var cum = new Array(length);
    var acc = 0;
    for (var i = 0; i < length; i += 1) {
      acc += charWeight(text.charAt(i));
      cum[i] = acc;
    }
    var total = acc;
    var start = null;

    function frame(ts) {
      if (start === null) start = ts;
      var elapsed = ts - start;
      var ratio = Math.min(1, elapsed / duration);
      var targetWeight = ratio * total;
      var count = 0;
      while (count < length && cum[count] <= targetWeight) count += 1;
      if (count === 0 && ratio > 0) count = 1;
      target.textContent = text.slice(0, count);
      if (ratio < 1) {
        window.requestAnimationFrame(frame);
      } else {
        target.textContent = text;
        if (onDone) onDone();
      }
    }
    window.requestAnimationFrame(frame);
  }

  function prepareTypewriter() {
    var nodes = Array.prototype.slice.call(document.querySelectorAll('[data-typewriter="true"]'));
    if (!nodes.length) return [];

    var reduced = prefersReducedMotion();

    nodes.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.height > 0) {
        el.style.minHeight = rect.height + "px";
      }

      if (reduced) {
        el.classList.add("is-complete");
        return;
      }

      var lineSpans = el.querySelectorAll(".typewriter-line");
      if (lineSpans.length) {
        el.__segments = Array.prototype.map.call(lineSpans, function (span) {
          return { el: span, text: span.textContent };
        });
        el.__segments.forEach(function (seg) { seg.el.textContent = ""; });
      } else {
        el.__fullText = el.textContent;
        el.textContent = "";
      }

      el.__typed = false;
    });

    return nodes;
  }

  function finishInstantly(el) {
    if (el.__segments) {
      el.__segments.forEach(function (seg) { seg.el.textContent = seg.text; });
    } else if (typeof el.__fullText === "string") {
      el.textContent = el.__fullText;
    }
    el.classList.remove("is-typing");
    el.classList.add("is-complete");
    el.__typed = true;
  }

  function runTypewriter(el) {
    if (el.__typed) return;
    el.__typed = true;
    el.classList.add("is-typing");

    if (el.__segments && el.__segments.length) {
      var idx = 0;
      (function nextSegment() {
        if (idx >= el.__segments.length) {
          el.classList.remove("is-typing");
          el.classList.add("is-complete");
          return;
        }
        var seg = el.__segments[idx];
        idx += 1;
        typeInto(seg.el, seg.text, LINE_DURATION_MS, function () {
          window.setTimeout(nextSegment, LINE_GAP_MS);
        });
      })();
    } else if (typeof el.__fullText === "string") {
      typeInto(el, el.__fullText, LINE_DURATION_MS, function () {
        el.classList.remove("is-typing");
        el.classList.add("is-complete");
      });
    } else {
      el.classList.remove("is-typing");
      el.classList.add("is-complete");
    }
  }

  function startObserving(nodes) {
    if (!nodes.length) return;
    var reduced = prefersReducedMotion();

    if (!("IntersectionObserver" in window)) {
      nodes.forEach(finishInstantly);
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          var el = entry.target;
          if (entry.isIntersecting && entry.intersectionRatio >= 0.12) {
            runTypewriter(el);
            observer.unobserve(el);
          }
        });
      },
      { threshold: [0, 0.12, 0.45, 1], rootMargin: "0px 0px -8% 0px" }
    );

    nodes.forEach(function (el) {
      if (reduced) return;
      observer.observe(el);
    });
  }

  function initAll() {
    // 先立刻把文字清空、記住原文，讓畫面一開始就是空白，
    // 不會閃現完整文字後又消失重打。
    var nodes = prepareTypewriter();

    // 封面（#report-hero-cover）用 position:fixed 蓋滿整個畫面，
    // 但底下文件流的位置並不會因此往下推，導致 IntersectionObserver
    // 在封面還蓋著時就誤判 #intro 已經「進入視窗」而提早開始打字。
    // 這裡等封面真的隱藏（使用者實際看得到內容）之後，才啟動觀察器
    // 去判斷「有沒有捲到這一頁」。
    var cover = document.getElementById("report-hero-cover");
    if (cover && !cover.hidden) {
      var waited = 0;
      var poll = window.setInterval(function () {
        waited += 60;
        if (!cover || cover.hidden || waited >= 8000) {
          window.clearInterval(poll);
          startObserving(nodes);
        }
      }, 60);
      return;
    }
    startObserving(nodes);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
