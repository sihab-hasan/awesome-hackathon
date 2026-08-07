(function () {
  function ensureProgressBar() {
    var bar = document.querySelector('.ah-reading-progress');
    if (!bar) {
      bar = document.createElement('div');
      bar.className = 'ah-reading-progress';
      document.body.appendChild(bar);
    }
    return bar;
  }

  function updateProgress() {
    var bar = ensureProgressBar();
    var root = document.documentElement;
    var max = root.scrollHeight - root.clientHeight;
    var value = max > 0 ? Math.min(100, Math.max(0, (root.scrollTop / max) * 100)) : 0;
    bar.style.width = value + '%';
  }

  document.addEventListener('scroll', updateProgress, { passive: true });
  document.addEventListener('DOMContentLoaded', updateProgress);
  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(updateProgress);
  }
})();
