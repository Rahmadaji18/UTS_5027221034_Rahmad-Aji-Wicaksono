function searchBooks() {
    var searchTerm = document.getElementById("searchInput").value;
    fetch("http://localhost:5051/search?query=" + searchTerm)
    .then(response => response.json())
    .then(data => {
        var books = data.books;
        var bookList = document.getElementById("bookList");
        bookList.innerHTML = "";
        books.forEach(book => {
            var title = book.title;
            var author = book.author_name ? book.author_name.join(", ") : "Unknown";
            var year = book.first_publish_year ? book.first_publish_year : "Unknown";
            var cover = book.cover_i ? `https://covers.openlibrary.org/b/id/${book.cover_i}-M.jpg` : "";
            
            var div = document.createElement("div");
            div.classList.add("book");
            div.innerHTML = `
                <img src="${cover}" alt="Book Cover">
                <div class="book-info">
                    <div class="book-title"><strong>${title}</strong></div>
                    <div class="author">Oleh ${author}</div>
                    <div class="year">Publikasi pertama pada tahun ${year}</div>
                    <button class="add-button" onclick="addToCollection('${title}', '${author}', '${year}')">Tambahkan ke Koleksi</button>
                </div>
            `;
            bookList.appendChild(div);
        });
    })
    .catch(error => console.error('Error:', error)); // Handle errors
}

function addToCollection(title, author, year) {
    var collectionList = document.getElementById("collectionList");
    var div = document.createElement("div");
    div.classList.add("book");
    div.innerHTML = `
        <div class="book-info">
            <div class="book-title"><strong>${title}</strong></div>
            <div class="author">Oleh ${author}</div>
            <button onclick="removeFromCollection(this)">Hapus dari Koleksi</button>
        </div>
    `;
    collectionList.appendChild(div);
}

function removeFromCollection(button) {
    button.parentElement.parentElement.remove();
}
