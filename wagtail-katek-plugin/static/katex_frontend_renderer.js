(() => {
  /**
  * This front end script looks for the KaTeX blocks inside completed Wagtail pages and renders them with KaTeX.
  */
  const katex = window.katex;
  const katexBlocks = [].slice.call(document.querySelectorAll('[data-katex-text]'));

  katexBlocks.forEach((block) => {
    window.katex.render(block.dataset.katexText, block)
  });
})();
