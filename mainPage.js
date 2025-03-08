document.addEventListener('DOMContentLoaded', function() {
    let currentImage = 1;
    const totalImages = 15;
    const responses = [];
    
    const displayedImage = document.getElementById('displayedImage');
    const crossButton = document.getElementById('crossButton');
    const tickButton = document.getElementById('tickButton');
    const progressDisplay = document.getElementById('progress');

    function updateImage() {
        if (currentImage <= totalImages) {
            displayedImage.src = `img/${currentImage}.jpg`;
            progressDisplay.textContent = `${currentImage}/${totalImages}`;
        } else {
            // All images have been processed
            displayedImage.style.display = 'none';
            crossButton.style.display = 'none';
            tickButton.style.display = 'none';
            progressDisplay.textContent = 'Complete!';
            console.log('Final responses:', responses);
        }
    }

    function handleResponse(response) {
        responses.push({
            imageNumber: currentImage,
            response: response
        });
        currentImage++;
        updateImage();
    }

    crossButton.addEventListener('click', () => handleResponse('cross'));
    tickButton.addEventListener('click', () => handleResponse('tick'));
});
