document.addEventListener('DOMContentLoaded', () => {
    const fileInputs = document.querySelectorAll('.file-input');
    const downloadButton = document.querySelector('.download-button');

    fileInputs.forEach((input, index) => {
        const textField = input.querySelector('input[type="text"]');
        const browseButton = input.querySelector('.browse-button');

        browseButton.addEventListener('click', () => {
            const fileInput = input.querySelector('input[type="file"]');
            fileInput.click();
            fileInput.addEventListener('change', (e) => {
                const selectedFile = e.target.files[0];
                textField.value = selectedFile.name;
                input.classList.add('completed');
            });
        });
    });

    downloadButton.addEventListener('click', () => {
        fileInputs.forEach((input) => {
            if (!input.classList.contains('completed')) {
                // Perform file upload and show progress view here
                // You may want to use AJAX or fetch to upload the file.
            }
        });

        // Download URLs with yt-dlp here
    });
});
