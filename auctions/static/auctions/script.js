// For bids list in listing page
const bidlistBtn = document.getElementById('bidlist-btn');
const bidlist = document.querySelector('#bidlist');

bidlistBtn.addEventListener('click', function(e) {
    bidlist.classList.toggle('visually-hidden');
})




