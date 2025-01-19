document.addEventListener('DOMContentLoaded', function() {

    // Get user balance on page load
    const userId = localStorage.getItem('user_id');
    if (userId) {
        // Check if the pop-up has been claimed before this session
        const popupShown = localStorage.getItem('popupShown');

        if (!popupShown) {
            // Show the free bet pop-up if it hasn't been shown yet
            showPopup();
        }

        // Fetch and display the user's balance
        axios.get(`http://127.0.0.1:5000/balance/${userId}`)
            .then(response => {
                document.getElementById('user-balance').textContent = response.data.balance;
            })
            .catch(error => {
                console.error('Failed to fetch balance:', error);
                document.getElementById('user-balance').textContent = 'Error loading balance';
            });
    } else {
        alert('User not logged in');
        window.location.href = "login.html";
    }

    // Slot machine spin function
    function spinSlotMachine(userId, betAmount) {
        if (!userId || !betAmount) {
            alert("User ID and bet amount are required.");
            return;
        }

        const slots = document.querySelectorAll('.slot');
        const miniSlots = document.querySelectorAll('.mini-slot');
        const slotImages = [
            "banana.png", "cherry.png", "diamond.png",
            "grapes.png", "lemon.png", "melon.png", "peach.png"
        ];

        let spins = 10; // Number of spins for animation
        let interval = setInterval(() => {
            // Animate slot images by randomly changing them every 100ms
            slots.forEach(slot => {
                const randomImage = slotImages[Math.floor(Math.random() * slotImages.length)];
                slot.src = `/static/casinoimg/${randomImage}`; // Dynamically change image
            });

            // Stop animation after the defined number of spins and fetch the actual result
            if (spins <= 0) {
                clearInterval(interval); // Stop the spin animation
                fetchSpinResult(userId, betAmount); // Fetch the actual result from the backend
            }
            spins--;
        }, 100); // Spin every 100ms
    }

    // Fetch the actual result after the animation
    function fetchSpinResult(userId, betAmount) {
        // Ensure betAmount is a number
        betAmount = Number(betAmount);

        // Validate betAmount to ensure it's a valid number
        if (isNaN(betAmount) || betAmount <= 0) {
            alert('Please enter a valid bet amount');
            return;
        }

        axios.post('http://127.0.0.1:5000/spin', {
            user_id: userId,
            bet_amount: betAmount
        })
        .then(response => {
            const result = response.data.spin_result; // Array of fruit names
            const win = response.data.win;
            const newBalance = response.data.balance;

            // Update the main slot machine images
            const slots = document.querySelectorAll('.slot');
            result.forEach((fruit, index) => {
                slots[index].src = `/static/casinoimg/${fruit}`; // Update image based on the result
            });

            // Update the mini slots in the result box
            const miniSlots = document.querySelectorAll('.mini-slot');
            result.forEach((fruit, index) => {
                miniSlots[index].src = `/static/casinoimg/${fruit}`;
            });

            // Display the result message
            document.getElementById('result').textContent = `${win > 0 ? 'You won!' : 'Try again!'}`;
            document.getElementById('user-balance').textContent = newBalance;
        })
        .catch(error => {
            console.error('Spin failed:', error); // Log the full error to the console for debugging
            alert('Spin failed: ' + (error.response?.data?.message || 'Unknown error'));
        });
    }

    // Add event listener for spin button click
    document.getElementById('spin-img').addEventListener('click', function() {
        const userId = localStorage.getItem('user_id');
        let betAmount = document.getElementById('bet-amount').value;

        // Validate bet amount input
        if (!betAmount || betAmount <= 0) {
            alert('Please enter a valid bet amount');
            return;
        }

        betAmount = Number(betAmount); // Convert betAmount to a number
        if (isNaN(betAmount)) {
            alert('Invalid bet amount. Please enter a valid number.');
            return;
        }

        spinSlotMachine(userId, betAmount); // Start the spin animation
    });

    // Show pop-up with falling coins animation and handle prize claiming
    function showPopup() {
        console.log('showPopup called');
        const popup = document.createElement('div');
        popup.classList.add('popup');
        console.log('Popup created:', popup);

        // Create popup content
        const popupContent = document.createElement('div');
        popupContent.classList.add('popup-content');

        const heading = document.createElement('h1');
        heading.textContent = "YOU'VE WON!";
        const message = document.createElement('p');
        message.textContent = "A £5 FREE BET!";
        const button = document.createElement('button');
        button.textContent = "Claim your prize";
        button.id = "claimButton";

        popupContent.appendChild(heading);
        popupContent.appendChild(message);
        popupContent.appendChild(button);
        popup.appendChild(popupContent);
        document.body.appendChild(popup);

        const coinsContainer = document.createElement('div');
        coinsContainer.classList.add('coins-container');
        document.body.appendChild(coinsContainer);

        // Create falling coins
        for (let i = 0; i < 20; i++) {
            let coin = document.createElement('div');
            coin.classList.add('coin');
            coin.style.left = `${Math.random() * 100}%`;  // Random horizontal position
            coin.style.animationDuration = `${Math.random() * 2 + 2}s`;  // Random falling speed
            coinsContainer.appendChild(coin);
        }

        // Show the popup by adding the 'visible' class
        popup.classList.add('visible');
        console.log('Popup is now visible:', popup.classList);

        // Add event listener to the claim button
        document.getElementById('claimButton').addEventListener('click', function() {
            // Hide the popup once the prize is claimed
            popup.classList.remove('visible'); // This hides the popup

            console.log('User ID:', localStorage.getItem('user_id')); 
            // Send the user's claim to the backend to update balance
            axios.post('http://127.0.0.1:5000/claim-prize', { // Backend endpoint to handle claiming the prize
                user_id: localStorage.getItem('user_id') //ensures user id is sent
            })
            .then(response => {
                console.log('Prize claimed:', response);
                // Set the flag to prevent popup from showing again in this session
                localStorage.setItem('popupShown', true);
                // Redirect to game page
                window.location.href = '/static/game.html';  // Change this to the correct page or route
            })
            .catch(error => {
                console.error('Error claiming prize:', error);
                alert('Error claiming your prize');
            });
        });
    }

    // Optional: Add a logout functionality to clear session data
    document.getElementById('logout-btn').addEventListener('click', function() {
        localStorage.removeItem('user_id');
        localStorage.removeItem('popupShown');
        window.location.href = "login.html"; // Redirect to login page
    });
});