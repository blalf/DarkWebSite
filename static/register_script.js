let usernames = [];

// Charger les usernames depuis le fichier JSON
fetch('/static/database.json')
    .then(response => response.json())
    .then(data => {
        usernames = data.users.map(user => user.username);

        // Sélectionner la balise datalist où les usernames seront ajoutés
        const datalist = document.getElementById('usernameList');

        // Ajouter chaque username à la datalist
        usernames.forEach(username => {
            const option = document.createElement('option');
            option.value = username;
            datalist.appendChild(option);
        });
    })
    .catch(error => console.error('Erreur lors du chargement du JSON:', error));


document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const usernameInput = document.getElementById('username');
    const usernameList = document.getElementById('usernameList');
    const creditCardInput = document.getElementById('credit_card_number');

    // Fetch user data from database.json
    fetch('/static/database.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const users = data.users;

            function updateDatalist(input, list) {
                const value = input.value.toLowerCase();
                list.innerHTML = '';
                users.forEach(user => {
                    if (user.username.toLowerCase().startsWith(value)) {
                        const option = document.createElement('option');
                        option.value = user.username;
                        list.appendChild(option);
                    }
                });
            }

            usernameInput.addEventListener('input', function() {
                updateDatalist(usernameInput, usernameList);
            });

            form.addEventListener('submit', function(event) {
                updateDatalist(usernameInput, usernameList);
                const username = usernameInput.value.toLowerCase();
                const userExists = users.some(user => user.username.toLowerCase() === username);

                if (userExists) {
                    event.preventDefault();
                    alert('Username already exists. Please choose a different username.');
                }
            });
        })
        .catch(error => console.error('Error fetching user data:', error));

    // Format credit card number input
    creditCardInput.addEventListener('input', function() {
        let value = creditCardInput.value.replace(/\D/g, ''); // Remove all non-digit characters
        value = value.match(/.{1,4}/g)?.join(' ') || ''; // Add space every 4 digits
        creditCardInput.value = value;
    });
});