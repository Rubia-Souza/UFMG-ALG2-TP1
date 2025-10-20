window.onload = () => {
    const searchButton = document.querySelector("#searchButton");
    const searchBox = document.querySelector("#searchBox");

    const loadingSection = document.querySelector("#loadingSection");

    const resultsSection = document.querySelector("#results");
    const noResultsSection = document.querySelector("#noResults");

    const paginationDiv = document.querySelector("#pagination");
    const prevButton = document.querySelector("#prevButton");
    const pageInfo = document.querySelector("#pageInfo");
    const nextButton = document.querySelector("#nextButton");

    let currentPage = 1;
    let totalPages = 1;
    let results = [];

    function handleError(status) {
        resultsSection.innerHTML = `<p class="error">An error occurred. Status code: ${status}</p>`;
    }

    function handleResponse(data) {
        function createResultItem(result) {
            const itemSection = document.createElement("div");
            itemSection.classList.add("result-item");

            const title = document.createElement("h2");
            title.textContent = result.title;
            itemSection.appendChild(title);

            const snippet = document.createElement("p");
            snippet.innerHTML = result.snippet;
            itemSection.appendChild(snippet);

            return itemSection;
        }

        function hasFoundResults(data) {
            return data && data[0] && data[0].title !== "No results found";
        }

        resultsSection.innerHTML = "";
        noResultsSection.style.display = "none";
        paginationDiv.style.display = "none";
        loadingSection.style.display = "none";
        nextButton.disabled = true;
        prevButton.disabled = true;
        
        if (!hasFoundResults(data)) {
            noResultsSection.style.display = "flex";
            resultsSection.innerHTML = "";
            return;
        }

        results = data;
        totalPages = Math.ceil(results.length / 10);
        currentPage = 1;
        
        if (totalPages > 1) {
            paginationDiv.style.display = "flex";
            nextButton.disabled = false;
            prevButton.disabled = true;
            pageInfo.textContent = `${currentPage}/${totalPages}`;
        } 
        else {
            paginationDiv.style.display = "none";
        }

        for (let i = 0; i < Math.min(10, results.length); i++) {
            const resultItem = createResultItem(results[i]);
            resultsSection.appendChild(resultItem);
        }

        nextButton.onclick = () => {
            if (currentPage >= totalPages) {
                return;
            }

            currentPage++;
            resultsSection.innerHTML = "";

            const startIndex = (currentPage - 1) * 10;
            const endIndex = Math.min(startIndex + 10, results.length);
            for (let i = startIndex; i < endIndex; i++) {
                const resultItem = createResultItem(results[i]);
                resultsSection.appendChild(resultItem);
            }

            prevButton.disabled = false;
            if (currentPage === totalPages) {
                nextButton.disabled = true;
            }
            pageInfo.textContent = `${currentPage}/${totalPages}`;
        };

        prevButton.onclick = () => {
            if (currentPage <= 1) {
                return;
            }

            currentPage--;
            resultsSection.innerHTML = "";
            
            const startIndex = (currentPage - 1) * 10;
            const endIndex = startIndex + 10;
            for (let i = startIndex; i < endIndex; i++) {
                const resultItem = createResultItem(results[i]);
                resultsSection.appendChild(resultItem);
            }

            nextButton.disabled = false;
            if (currentPage === 1) {
                prevButton.disabled = true;
            }
            pageInfo.textContent = `${currentPage}/${totalPages}`;
        };
    }

    function fetchResults() {
        const expression = searchBox.value.trim();
        if (expression === "") {
            return;
        }

        loadingSection.style.display = "flex";
        resultsSection.innerHTML = "";
        noResultsSection.style.display = "none";
        paginationDiv.style.display = "none";

        fetch(`/search?expression=${encodeURIComponent(expression)}`)
            .then(response => {
                if (!response.ok) {
                    handleError(response.status);
                }
    
                return response.json();
            })
            .then(data => {
                handleResponse(data);
            })
            .catch(error => {
                console.error("Error fetching results:", error);
                handleError("Network error");
            });
    }

    searchButton.addEventListener("click", fetchResults);
    searchBox.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            fetchResults();
        }
    });
};
