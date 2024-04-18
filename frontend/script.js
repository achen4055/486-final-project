document.addEventListener('DOMContentLoaded', function() {
    fetch('books_recommend.json')
    .then(response => response.json())
    .then(data => displayBooks(data))
    .catch(error => console.error('Error loading the JSON file:', error));
});

function displayBooks(bookData) {
    const booksContainer = document.getElementById('books');

    Object.entries(bookData).forEach(([category, books]) => {
        const categoryElem = document.createElement('div');
        categoryElem.className = 'col-12';
        categoryElem.innerHTML = `<h2 class="mt-4">${category}</h2>`;
        booksContainer.appendChild(categoryElem);

        const bookRow = document.createElement('div');
        bookRow.className = 'row';
        categoryElem.appendChild(bookRow);

        Object.entries(books).forEach(([title, book]) => {
            const bookElem = document.createElement('div');
            bookElem.className = 'col-sm-6 col-md-4 col-lg-3 mb-4';
            bookElem.innerHTML = `
                <div class="card h-100">
                    <img src="${book.image.thumbnail}" class="card-img-top" alt="${title}">
                    <div class="card-body">
                        <h5 class="card-title">${title}</h5>
                        <p class="card-text">Authors: ${book.authors.join(', ')}</p>
                        <p class="card-text">Published Date: ${book.published_date}</p>
                        <p class="card-text">Price: ${book.sale_price ? `$${book.sale_price}` : 'Not available'}</p>
                        <button type="button" class="btn btn-primary toggle-description">Show Description</button>

                        <div class="description">${book.description}</div>
                    </div>
                </div>
            `;
            bookRow.appendChild(bookElem);
        });
    });
    addToggleDescriptionEventListeners();
}

function addToggleDescriptionEventListeners() {
    document.querySelectorAll('.toggle-description').forEach(button => {
        button.addEventListener('click', function() {
            const descriptionDiv = this.nextElementSibling;
            if (descriptionDiv.style.display === 'none') {
                descriptionDiv.style.display = 'block';
                this.textContent = 'Hide Description'; // 更新按钮文本
            } else {
                descriptionDiv.style.display = 'none';
                this.textContent = 'Show Description'; // 更新按钮文本
            }
        });
    });
}
