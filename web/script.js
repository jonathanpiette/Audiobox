function browseForFile() {
    const fileInput = document.getElementById("file-upload");
    fileInput.click(); // Trigger the file input click event when the "Browse" button is clicked.
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            document.getElementById("file-input").value = file.name;
            document.getElementById("file-icon").style.display = "inline"; // Show the file icon.
        }
    });
}

const fileInput = document.getElementById("file-input");
const fileIcon = document.getElementById("file-icon");

fileInput.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.stopPropagation();
});

fileInput.addEventListener("dragenter", () => {
    fileInput.classList.add("dragover");
});

fileInput.addEventListener("dragleave", () => {
    fileInput.classList.remove("dragover");
});

fileInput.addEventListener("drop", (e) => {
    e.preventDefault();
    e.stopPropagation();
    fileInput.classList.remove("dragover");

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        fileInput.value = file.name;
        fileIcon.style.display = "inline"; // Show the file icon.
    }
});

// Listen for changes to the file input
fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
        fileIcon.style.display = "inline"; // Show the file icon.
    }
});

