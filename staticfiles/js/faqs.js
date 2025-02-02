function toggleAnswer(element) {
    let answer = element.nextElementSibling;
    if (answer.style.display === "none" || answer.style.display === "") {
        answer.style.display = "block";
        element.querySelector('span').innerHTML = "&#9650;"; 
    } else {
        answer.style.display = "none";
        element.querySelector('span').innerHTML = "&#9660;"; 
    }
}

function redirectToEdit(faqId) {
    window.location.href = window.location.href+`edit/?faq_id=${faqId}`; 
}