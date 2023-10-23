function browseForFile() {
    const fileInput = document.getElementById("file-upload");
    const fileUpload = document.getElementById('file-upload');

    fileInput.click(); // Trigger the file input click event when the "Browse" button is clicked.
    // fileUpload.click(); // Trigger the file input click event when the "Browse" button is clicked.

    fileInput.addEventListener("change", function () {
        const fileList = fileUpload.files;
        const fileListContainer = document.getElementById('file-list');
        // Clear the previous list
        fileListContainer.innerHTML = '';
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            document.getElementById("file-input").value = file.name;
            
        }

        for (const file of fileList) {
            const fileIcon = document.createElement('img');
            const cancelIcon = document.createElement('img');
            const listItem = document.createElement('li');
            const listContainer = document.createElement('div'); // Create a container for the elements


            fileIcon.classList.add('file-icon');
            cancelIcon.classList.add('cancel-icon');
            listContainer.classList.add('list-container')
            
            fileIcon.src = 'file-icon.png';
            cancelIcon.src = 'cancel-icon.png';

            listItem.textContent = file.name;

            // Add the elements to the container
            listContainer.appendChild(fileIcon);
            listContainer.appendChild(listItem);
            listContainer.appendChild(cancelIcon);

            fileListContainer.appendChild(listContainer);
        }
    });
}

// Add event listener for the cancel icon
// cancelIcon.addEventListener("click", () => {
//     fileInput.value = ''; // Clear the file input field
//     // cancelIcon.style.display = 'none'; // Hide the cancel icon
//     // fileIcon.style.display = 'none'; // Hide the file icon
// });

