function pdf_file(url, selector) {
  const task = pdfjsLib.getDocument(url);
  const container = document.querySelector(selector);
  while (container.firstChild) {
    container.removeChild(container.firstChild);
  }
  const row = document.createElement('div');
  row.classList = 'row overflow-hidden h-100';
  const pages = document.createElement('div');
  pages.classList = 'col col-md-2 d-flex flex-column gap-2 overflow-auto h-100';
  const currentPage = document.createElement('div');
  currentPage.classList = 'col col-md-10  d-flex flex-column';
  row.appendChild(pages);
  row.appendChild(currentPage);
  container.appendChild(row);

  task.promise
    .then((pdf) => {
      const pageNumber = 1;
      const renderPage = (page) => {
        const curPage = document.createElement('canvas');
        currentPage.innerText = '';
        currentPage.appendChild(curPage);
        const viewport = page.getViewport({
          scale: 1.5,
        });
        const context = curPage.getContext('2d');
        curPage.height = viewport.height;
        curPage.width = viewport.width;
        const renderContext = {
          canvasContext: context,
          viewport: viewport
        };
        const rt = page.render(renderContext);
        rt.promise.then(() => {
          const br = curPage.getBoundingClientRect();
          container.style.height = `${br.height}px`;
        })
      }
      const pagesData = Promise.allSettled([...Array(pdf.numPages)].map((_, pageNumber) => pdf.getPage(pageNumber + 1)))
        .then((r) => r.map((pageResult, i) => {
          if (pageResult.status === 'fulfilled') {
            const page = pageResult.value;
            const curPagePreview = document.createElement('canvas');
            pages.appendChild(curPagePreview);
            curPagePreview.style.cursor = 'pointer';
            const viewport = page.getViewport({
              scale: 0.2,
            });
            const context = curPagePreview.getContext('2d');
            curPagePreview.height = viewport.height;
            curPagePreview.width = viewport.width;
            const renderContext = {
              canvasContext: context,
              viewport: viewport
            };
            page.render(renderContext);
            curPagePreview.addEventListener('click', () => renderPage(page));
            if (i === 0) renderPage(page);
          }
        }));

    })
    .catch((e) => console.error(e));
}