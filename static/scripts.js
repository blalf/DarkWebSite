// Obtenez le popup
var popup = document.getElementById("loginPopup");

// Obtenez le bouton qui ouvre le popup
var btn = document.getElementById("loginBtn");

// Obtenez l'élément <span> qui ferme le popup
var span = document.getElementsByClassName("close")[0];

// Lorsque l'utilisateur clique sur le bouton, ouvrez le popup
btn.onclick = function() {
    popup.style.display = "block";
}

// Lorsque l'utilisateur clique sur <span> (x), fermez le popup
span.onclick = function() {
    popup.style.display = "none";
}

// Lorsque l'utilisateur clique n'importe où en dehors du popup, fermez-le
window.onclick = function(event) {
    if (event.target == popup) {
        popup.style.display = "none";
    }
}


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
    const form = document.getElementById('form_login');
    const errorMessageDiv = document.getElementById('error_message');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                errorMessageDiv.textContent = data.error_message;
            }
        })
        .catch(error => console.error('Error:', error));
    });
});


function addToCart(productId) {
    const form = document.getElementById(`add-to-cart-form-${productId}`);
    const formData = new FormData(form);

    fetch('/add_to_cart', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();  // Reload the current page
        } else {
            alert('Erreur: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}