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
    const urlParams = new URLSearchParams(window.location.search);
    const lang = urlParams.get('lang');  

    if (lang) {
        window.location.href = `${window.location.origin}/faqs/edit/?lang=${lang}&faq_id=${faqId}`;
    } else {
        window.location.href = `${window.location.origin}/faqs/edit/?faq_id=${faqId}`;
    }
}

function changeLanguage() {
    var selectedLang = document.getElementById("language-select").value;
    window.location.href = "?lang=" + selectedLang;
}