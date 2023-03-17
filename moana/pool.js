// Pull from this page
// https://www.dunedin.govt.nz/news-and-events/public-notices/moana-pool-timetable
// Get the PDF that corresponds to today
// Convert PDF to data which can be processed
// Process data to create a timeseries plot


function getLinksFromUrl(url) {
    fetch(url, {mode: 'no-cors'})
      .then(response => response.text())
      .then(html => {
        // Parse the HTML content using the DOMParser API
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
  
        // Extract all the links from the document
        const links = doc.querySelectorAll('a');
        const linkUrls = Array.from(links).map(link => link.href);
  
        // Log the links to the console
        console.log(linkUrls);
      })
      .catch(error => console.error(error));
  }
  
  // Example usage
  getLinksFromUrl('https://www.dunedin.govt.nz/news-and-events/public-notices/moana-pool-timetable');