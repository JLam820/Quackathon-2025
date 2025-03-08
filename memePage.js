// Meme data with categorizations
const memeData = [
    {
      id: 1,
      categories: {
        'A': 1, 'D': 2, 'W': 3, 'S': 4, 
        'L': 5, 'P': 4, 'C': 3, 'R': 2
      }
    },
    {
      id: 2,
      categories: {
        'A': 4, 'D': 1, 'W': 1, 'S': 4, 
        'L': 1, 'P': 0, 'C': 3, 'R': 5
      }
    },
    {
        id: 3,
        categories: {
          'A': 5, 'D': 2, 'W': 3, 'S': 2, 
          'L': 1, 'P': 4, 'C': 3, 'R': 2
        }
      },
      {
        id: 4,
        categories: {
          'A': 1, 'D': 2, 'W': 1, 'S': 4, 
          'L': 0, 'P': 3, 'C': 3, 'R': 2
        }
      },
      {
        id: 5,
        categories: {
          'A': 4, 'D': 2, 'W': 3, 'S': 3, 
          'L': 0, 'P': 2, 'C': 5, 'R': 2
        }
      },

  ];
  
  // Humor categories 
  const humorCategories = {
    'A': {
      name: 'Absurdist/Surreal',
      description: 'You enjoy humor that breaks reality and creates its own bizarre logic',
      color: '#ff9800'  // ADD THIS LINE
    },
    'D': {
      name: 'Dark',
      description: 'You appreciate edgy humor that flirts with the controversial',
      color: '#424242'
    },
    'W': {
      name: 'Wholesome',
      description: 'You love uplifting, positive humor that makes everyone feel good',
      color: '#4caf50'
    },
    'S': {
      name: 'Sarcastic/Dry',
      description: 'You enjoy witty, deadpan humor that often involves irony',
      color: '#ffeb3b'
    },
    'L': {
      name: 'Self-Deprecating',
      description: 'You appreciate humor that doesn\'t take itself too seriously',
      color: '#9c27b0'
    },
    'P': {
      name: 'Slapstick/Physical',
      description: 'You enjoy visual gags and exaggerated physical humor',
      color: '#f44336'
    },
    'C': {
      name: 'Clever/Wordplay',
      description: 'You appreciate intellectual humor, including puns and linguistic plays',
      color: '#3f51b5'
    },
    'R': {
      name: 'Random/Dank',
      description: 'You enjoy chaotic, unpredictable humor typical of internet culture',
      color: '#795548'
    }
  };
  
let currentImage = 1;
const totalImages = memeData.length;
const responses = [];
let currentRating = null;
let userScores = {
    'A': 0, 'D': 0, 'W': 0, 'S': 0, 
    'L': 0, 'P': 0, 'C': 0, 'R': 0
};

// DOM elements
const displayedImage = document.getElementById('displayedImage');
const ratingButtons = document.querySelectorAll('.rating-button');
const submitButton = document.getElementById('submit-button');
const progressDisplay = document.getElementById('progress');
const resultsDiv = document.getElementById('results');
const finalHumorCode = document.getElementById('final-humor-code');
const humorCodesContainer = document.getElementById('humor-codes-container');
const humorDescription = document.getElementById('humor-description');
const shareButton = document.getElementById('share-button');

// Update image and progress
function updateImage() {
    if (currentImage <= totalImages) {
        // Update the image (force browser to reload by adding timestamp)
        displayedImage.src = `img/${currentImage}.jpg?t=${new Date().getTime()}`;
        progressDisplay.textContent = `${currentImage}/${totalImages}`;
        
        // Reset rating buttons
        ratingButtons.forEach(button => button.classList.remove('selected'));
        submitButton.classList.remove('active');
        currentRating = null;
    } else {
        // All images have been processed, show results
        document.querySelector('.container').style.display = 'none';
        showResults();
    }
}

// Handle user's response
function handleResponse() {
    // Get current meme data
    const meme = memeData.find(m => m.id === currentImage) || memeData[currentImage - 1];
    
    // Record response
    responses.push({
        memeId: meme.id,
        rating: currentRating
    });
    
    // Update scores by multiplying each category by user's rating
    for (const [category, score] of Object.entries(meme.categories)) {
        userScores[category] += score * currentRating;
    }
    
    // Move to next image
    currentImage++;
    updateImage();
}

// Get top N categories based on scores
function getTopCategories(n = 3) {
    // Sort categories by score (descending)
    const sortedCategories = Object.entries(userScores)
        .sort((a, b) => b[1] - a[1])
        .map(entry => entry[0]);
    
    // Return top N categories
    return sortedCategories.slice(0, n);
}

// Show final results
function showResults() {
    // Get top 3 categories
    const topCategories = getTopCategories(3);
    const humorCode = topCategories.join('');
    
    // Display the code
    finalHumorCode.textContent = humorCode;
    
    // Create elements for each category
    humorCodesContainer.innerHTML = '';
    topCategories.forEach(category => {
        const categoryEl = document.createElement('div');
        categoryEl.className = 'humor-code';
        categoryEl.style.backgroundColor = humorCategories[category].color;
        
        categoryEl.innerHTML = `
            <span class="code">${category}</span>
            <span class="name">${humorCategories[category].name}</span>
        `;
        
        humorCodesContainer.appendChild(categoryEl);
    });
    
    // Create description
    let description = "You have a unique sense of humor that combines:\n";
    topCategories.forEach(category => {
        description += `• ${humorCategories[category].name}: ${humorCategories[category].description}\n`;
    });
    
    humorDescription.innerHTML = description.replace(/\n/g, '<br>');
    
    // Show results
    resultsDiv.style.display = 'flex';
    
    // Save humor code to localStorage (for potential future use)
    localStorage.setItem('userHumorCode', humorCode);
    localStorage.setItem('userHumorScores', JSON.stringify(userScores));
    localStorage.setItem('userHumorResponses', JSON.stringify(responses));

    console.log('Final scores:', userScores);
    console.log('Humor code:', humorCode);
    console.log('All responses:', responses);
}

// Add event listeners to rating buttons
ratingButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove selected class from all buttons
        ratingButtons.forEach(btn => btn.classList.remove('selected'));
        // Add selected class to clicked button
        button.classList.add('selected');
        currentRating = parseInt(button.dataset.rating);
        submitButton.classList.add('active');
    });
});

// Add event listener to submit button
submitButton.addEventListener('click', () => {
    if (currentRating !== null) {
        handleResponse();
    }
});

// Add event listener to share button
shareButton.addEventListener('click', () => {
    const humorCode = getTopCategories(3).join('');
    alert(`Your humor code is: ${humorCode}`);
});

// Initialize
updateImage();