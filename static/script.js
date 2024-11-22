// Ambil elemen input dan elemen untuk menampilkan nama file
const fileInput = document.getElementById("file-upload");
const fileNameDisplay = document.getElementById("file-name");

// Event listener untuk input file
fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
        // Jika file dipilih, tampilkan nama file
        fileNameDisplay.textContent = `File yang dipilih: ${fileInput.files[0].name}`;
    } else {
        // Jika tidak ada file, tampilkan teks default
        fileNameDisplay.textContent = "Format yang didukung: JPG dan PNG";
    }
});

