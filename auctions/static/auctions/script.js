// For bids list in listing page
const bidlistBtn = document.querySelector('#bidlist-btn');
const bidlist = document.querySelector('#bidlist');

if (bidlistBtn) {
    bidlistBtn.addEventListener('click', function(e) {
        bidlist.classList.toggle('visually-hidden');
    });
}

// For tabs
const tab1 = document.querySelector('#tab-1');
const tab2 = document.querySelector('#tab-2');

const tabItem1 = document.querySelector('#tab-item-1');
const tabItem2 = document.querySelector('#tab-item-2');

if (tab1) {
    tab1.addEventListener('click', function(e) {
        if (!tab1.classList.contains('active')) {
            tab1.classList.toggle('active');
            tab2.classList.toggle('active');
            tabItem1.classList.toggle('visually-hidden');
            tabItem2.classList.toggle('visually-hidden');
        }

    });

    tab2.addEventListener('click', function(e) {
        if (!tab2.classList.contains('active')) {
            tab1.classList.toggle('active')
            tab2.classList.toggle('active');
            tabItem1.classList.toggle('visually-hidden');
            tabItem2.classList.toggle('visually-hidden');
        }

    });
}

// For images
const imgs = document.querySelectorAll('.img');

function swipe_right() {
    
}

function swipe_left() {

}



