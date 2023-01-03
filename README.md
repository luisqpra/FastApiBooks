<h1>FastApiBooks, API Endpoints</h1>
<p>This API has the following endpoints:</p>
<h2>GET /</h2>
<p>Returns a simple message.</p>
<h2>POST /book/new</h2>
<p>Creates a new book and returns it.</p>
<h3>Input</h3>
<ul>
  <li>
    <p><code>book</code>: A <code>Book</code> object with the following attributes:</p>
    <ul>
      <li><code>title</code> (required, string): Title of the book.</li>
      <li><code>author</code> (required, string): Author of the book.</li>
      <li><code>reading_age</code> (optional, <code>ReadingAge</code> enum): Reading age of the book.</li>
      <li><code>pages</code> (optional, integer): Number of pages in the book.</li>
      <li><code>language</code> (optional, <code>Language</code> enum): Language of the book.</li>
      <li><code>publisher</code> (optional, string): Publisher of the book.</li>
      <li><code>isbn_10</code> (required, string): ISBN-10 code of the book.</li>
      <li><code>id_hide</code> (required, string): A hidden ID for the book.</li>
    </ul>
  </li>
</ul>
<h3>Output</h3>
<p>A <code>BookOut</code> object with the following attributes:</p>
<ul>
  <li><code>title</code> (string): Title of the book.</li>
  <li><code>author</code> (string): Author of the book.</li>
  <li><code>reading_age</code> (<code>ReadingAge</code> enum):
