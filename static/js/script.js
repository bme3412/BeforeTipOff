<script src="{{ url_for('static', filename='js/script.js') }}"></script>
document.addEventListener('DOMContentLoaded', function() {
    var searchButton = document.getElementById('search-btn');
    searchButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default form submission
        var form = document.querySelector('form');
        form.submit(); // Programmatically submit the form
    });
});
