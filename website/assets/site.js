/* Bear Lake Montessori Academy — shared interactions */
(function () {
  'use strict';
  var doc = document;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };
  var SCHOOL_EMAIL = 'bearlakemontessori@gmail.com';

  /* ---------- Mobile menu ---------- */
  var menuBtn = $('.menu-btn');
  var mobileNav = $('#mobile-nav');
  function setMenu(open) {
    if (!menuBtn || !mobileNav) return;
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    menuBtn.textContent = open ? 'Close' : 'Menu';
    mobileNav.hidden = !open;
    doc.body.classList.toggle('menu-open', open);
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () { setMenu(mobileNav.hidden); });
    $$('a', mobileNav).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    window.addEventListener('resize', function () { if (window.innerWidth >= 1060) setMenu(false); });
  }

  /* ---------- Desktop dropdowns (click/touch + keyboard) ---------- */
  $$('.nav-item[data-dropdown]').forEach(function (item) {
    var btn = $('.nav-link', item);
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var open = !item.classList.contains('open');
      $$('.nav-item.open').forEach(function (o) { o.classList.remove('open'); $('.nav-link', o).setAttribute('aria-expanded', 'false'); });
      item.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  doc.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-item')) $$('.nav-item.open').forEach(function (o) { o.classList.remove('open'); $('.nav-link', o).setAttribute('aria-expanded', 'false'); });
  });
  doc.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    $$('.nav-item.open').forEach(function (o) { o.classList.remove('open'); var b = $('.nav-link', o); b.setAttribute('aria-expanded', 'false'); b.focus(); });
    if (mobileNav && !mobileNav.hidden) { setMenu(false); menuBtn.focus(); }
  });

  /* ---------- Scroll reveal ---------- */
  var revealEls = $$('[data-reveal]');
  if (!('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.setAttribute('data-reveal', 'in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.setAttribute('data-reveal', 'in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Parallax + cursor drift ---------- */
  if (!reduce) {
    var parallax = $$('[data-parallax]');
    if (parallax.length) {
      var ticking = false;
      window.addEventListener('scroll', function () {
        if (ticking) return; ticking = true;
        requestAnimationFrame(function () {
          var y = Math.min(window.scrollY, 1400);
          parallax.forEach(function (el) { el.style.transform = 'translateY(' + (y * parseFloat(el.dataset.parallax)).toFixed(1) + 'px)'; });
          ticking = false;
        });
      }, { passive: true });
    }
    var drift = $$('[data-drift]');
    if (drift.length && window.matchMedia('(pointer:fine)').matches) {
      var mx = 0, my = 0, raf = 0;
      window.addEventListener('mousemove', function (e) {
        mx = e.clientX / window.innerWidth - 0.5; my = e.clientY / window.innerHeight - 0.5;
        if (raf) return;
        raf = requestAnimationFrame(function () {
          drift.forEach(function (el) { var f = parseFloat(el.dataset.drift); el.style.transform = 'translate(' + (mx * f).toFixed(1) + 'px,' + (my * f).toFixed(1) + 'px)'; });
          raf = 0;
        });
      }, { passive: true });
    }
  }

  /* ---------- Enquiry forms ----------
     The school books tours by phone and email, so forms compose an email
     to the school in the visitor's own mail app — nothing is stored here. */
  $$('form[data-enquiry]').forEach(function (form) {
    var done = $('.form-done', form.parentNode) || $('.form-done', form);
    var err = $('.form-error', form);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = new FormData(form);
      var lines = [];
      var subject = form.getAttribute('data-subject') || 'Enquiry from the website';
      $$('[name]', form).forEach(function (f) {
        if (f.type === 'radio' && !f.checked) return;
        if (f.type === 'checkbox' && !f.checked) return;
        var v = (f.value || '').trim(); if (!v) return;
        var label = f.getAttribute('data-label') || f.name;
        if (lines.some(function (l) { return l.indexOf(label + ':') === 0; }) && f.type !== 'checkbox') return;
        lines.push(label + ': ' + v);
      });
      var name = (data.get('name') || '').toString().trim();
      if (name) subject += ' — ' + name;
      var href = 'mailto:' + SCHOOL_EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n') + '\n\nSent from bearlakemontessori.com');
      if (err) err.hidden = true;
      window.location.href = href;
      if (done) {
        var fields = $('.fields', form);
        if (fields) fields.hidden = true;
        done.hidden = false;
        done.setAttribute('tabindex', '-1'); done.focus({ preventScroll: true });
      }
    });
  });

  /* ---------- Gallery: filter + lightbox ---------- */
  var gallery = $('[data-gallery]');
  if (gallery) {
    var plates = $$('.plate', gallery);
    var filters = $$('[data-filter]');
    var count = $('[data-gallery-count]');
    filters.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter');
        filters.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        var shown = 0;
        plates.forEach(function (p) {
          var on = f === 'all' || (p.getAttribute('data-cat') || '').split(' ').indexOf(f) > -1;
          p.hidden = !on; if (on) shown++;
        });
        if (count) count.textContent = shown + (shown === 1 ? ' photo' : ' photos');
      });
    });
    var lb = $('#lightbox');
    if (lb && typeof lb.showModal === 'function') {
      var img = $('.lb-img', lb), cap = $('.lb-cap', lb), idx = 0;
      var visible = function () { return plates.filter(function (p) { return !p.hidden; }); };
      var show = function (i) {
        var list = visible(); if (!list.length) return;
        idx = (i + list.length) % list.length;
        var p = list[idx], pi = $('img', p);
        img.src = pi.getAttribute('src'); img.alt = pi.alt;
        cap.innerHTML = '';
        cap.appendChild(doc.createTextNode($('figcaption', p).textContent));
        var sm = doc.createElement('small'); sm.textContent = pi.alt + ' · ' + (idx + 1) + ' of ' + list.length; cap.appendChild(sm);
      };
      plates.forEach(function (p) {
        $('.plate-btn', p).addEventListener('click', function () { show(visible().indexOf(p)); lb.showModal(); });
      });
      $('[data-lb="prev"]', lb).addEventListener('click', function () { show(idx - 1); });
      $('[data-lb="next"]', lb).addEventListener('click', function () { show(idx + 1); });
      $('[data-lb="close"]', lb).addEventListener('click', function () { lb.close(); });
      lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
      lb.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') show(idx - 1);
        if (e.key === 'ArrowRight') show(idx + 1);
      });
    }
  }

  /* ---------- Tabs (curriculum areas) ---------- */
  $$('[role="tablist"]').forEach(function (list) {
    var tabs = $$('[role="tab"]', list);
    var select = function (t, focus) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute('aria-selected', on ? 'true' : 'false');
        x.tabIndex = on ? 0 : -1;
        var panel = doc.getElementById(x.getAttribute('aria-controls'));
        if (panel) panel.hidden = !on;
      });
      if (focus) t.focus();
      if (history.replaceState && t.dataset.hash) history.replaceState(null, '', '#' + t.dataset.hash);
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        if (e.key === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === 'Home') n = tabs[0];
        if (e.key === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
    var fromHash = function () {
      var h = location.hash.slice(1);
      var t = tabs.filter(function (x) { return x.dataset.hash === h; })[0];
      if (t) { select(t); list.scrollIntoView({ block: 'start', behavior: reduce ? 'auto' : 'smooth' }); }
    };
    fromHash();
    window.addEventListener('hashchange', fromHash);
  });

  /* ---------- FAQ search + topics ---------- */
  var faqRoot = $('[data-faq]');
  if (faqRoot) {
    var items = $$('.faq', faqRoot);
    var groups = $$('[data-faq-group]', faqRoot);
    var q = $('#faq-search');
    var topicBtns = $$('[data-topic]');
    var empty = $('[data-faq-empty]');
    var topic = 'all';
    var apply = function () {
      var term = (q && q.value || '').trim().toLowerCase();
      var any = 0;
      items.forEach(function (it) {
        var g = it.closest('[data-faq-group]').getAttribute('data-faq-group');
        var match = (topic === 'all' || g === topic) && (!term || it.textContent.toLowerCase().indexOf(term) > -1);
        it.hidden = !match; if (match) any++;
        if (term && match) it.open = true;
      });
      groups.forEach(function (g) { g.hidden = !$$('.faq', g).some(function (it) { return !it.hidden; }); });
      if (empty) empty.hidden = any > 0;
    };
    if (q) q.addEventListener('input', apply);
    topicBtns.forEach(function (b) {
      b.addEventListener('click', function () {
        topic = b.getAttribute('data-topic');
        topicBtns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        apply();
      });
    });
  }

  /* ---------- Hotspots ---------- */
  $$('[data-hotspots]').forEach(function (root) {
    var pins = $$('.pin', root), rows = $$('[data-pin]', root);
    var set = function (n) {
      pins.forEach(function (p) { p.classList.toggle('is-on', p.getAttribute('data-for') === n); });
      rows.forEach(function (r) { r.classList.toggle('is-on', r.getAttribute('data-pin') === n); });
    };
    pins.forEach(function (p) {
      ['mouseenter', 'focus', 'click'].forEach(function (ev) { p.addEventListener(ev, function () { set(p.getAttribute('data-for')); }); });
    });
    rows.forEach(function (r) { r.addEventListener('mouseenter', function () { set(r.getAttribute('data-pin')); }); });
    root.addEventListener('mouseleave', function () { set(null); });
  });

  /* ---------- Horizontal strip controls ---------- */
  $$('[data-strip]').forEach(function (wrap) {
    var strip = $('.strip', wrap);
    $$('[data-strip-dir]', wrap).forEach(function (b) {
      b.addEventListener('click', function () {
        var card = strip.firstElementChild;
        var step = card ? card.getBoundingClientRect().width + 24 : 320;
        strip.scrollBy({ left: step * parseInt(b.getAttribute('data-strip-dir'), 10), behavior: reduce ? 'auto' : 'smooth' });
      });
    });
  });

  /* ---------- Mobile swipe rows: position dots ---------- */
  var phone = window.matchMedia('(max-width:640px)');
  $$('.m-swipe').forEach(function (row) {
    var items = Array.prototype.slice.call(row.children);
    if (items.length < 2) return;
    var dots = doc.createElement('div');
    dots.className = 'swipe-dots';
    dots.setAttribute('aria-hidden', 'true');
    items.forEach(function () { dots.appendChild(doc.createElement('span')); });
    row.parentNode.insertBefore(dots, row.nextSibling);
    var marks = Array.prototype.slice.call(dots.children);
    var update = function () {
      var max = row.scrollWidth - row.clientWidth;
      dots.style.display = phone.matches && max > 4 ? '' : 'none';
      var i = max > 0 ? Math.round((row.scrollLeft / max) * (items.length - 1)) : 0;
      marks.forEach(function (m, k) { m.classList.toggle('on', k === i); });
    };
    var t = 0;
    row.addEventListener('scroll', function () { if (!t) t = requestAnimationFrame(function () { update(); t = 0; }); }, { passive: true });
    window.addEventListener('resize', update);
    update();
  });

  /* ---------- Mobile quick-action bar ---------- */
  var mbar = $('.m-bar');
  if (mbar) {
    var blockers = new Set();
    var scrolled = false;
    var sync = function () { mbar.classList.toggle('show', scrolled && blockers.size === 0); };
    window.addEventListener('scroll', function () {
      var s = window.scrollY > window.innerHeight * 0.6;
      if (s !== scrolled) { scrolled = s; sync(); }
    }, { passive: true });
    if ('IntersectionObserver' in window) {
      var bo = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) blockers.add(en.target); else blockers.delete(en.target); });
        sync();
      }, { rootMargin: '0px 0px -10% 0px' });
      $$('[data-hide-mbar]').forEach(function (el) { bo.observe(el); });
    }
  }

  /* ---------- Footer year ---------- */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
