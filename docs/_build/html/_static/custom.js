// Show or hide the button based on scroll position
window.addEventListener('scroll', function() {
    var button = document.getElementById('scroll-to-top');
    if (window.scrollY > 200) { // Adjust the value as needed
        button.style.display = 'block';
    } else {
        button.style.display = 'none';
    }
});

// Smooth scroll to the top when the button is clicked
document.getElementById('scroll-to-top').addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});
