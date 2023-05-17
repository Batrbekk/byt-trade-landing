




    

    



//Accordeon FAQ

const tabletItemsFAQ = document.querySelectorAll('.Tablet_item_FAQ');

tabletItemsFAQ.forEach(itemFAQ => {
const titleFAQ = itemFAQ.querySelector('.Tablet-title_FAQ');
const textFAQ = itemFAQ.querySelector('.Mobile_tablet_text_FAQ');

titleFAQ.addEventListener('click', () => {
    textFAQ.classList.toggle('opened');
    itemFAQ.classList.toggle('opened');
    titleFAQ.classList.toggle('opened');
});


});


