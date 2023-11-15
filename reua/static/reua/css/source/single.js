function changeImage(imageSrc) {
	const mainImage = document.querySelector('.single__wrapper .main-image img');
	mainImage.src = imageSrc;
	mainImage.alt = imageSrc;
}

// =============
// Preloader
// =============

var videos = document.querySelectorAll("video");
var startTime = Date.now(); // Время начала отсчета
var timerElement = document.getElementById("percents");

function updatePercent() {
	var currentTime = Date.now();
	var elapsedTime = currentTime - startTime;
	var percent = (elapsedTime / 5000) * 100; // 5 секунд
	if (percent > 100) {
		percent = 100;
	}
	timerElement.textContent = Math.round(percent);
}

var timerInterval = setInterval(updatePercent, 100); // Обновляем процент каждые 5 секунд

setTimeout(function () {
	clearInterval(timerInterval);
	var preloader = document.getElementById("preloader");
	preloader.classList.add("preloader--hide");
}, 5000);






document.addEventListener('DOMContentLoaded', function () {
	const thumbnailsList = document.querySelector('.thumbnails-list');
	const thumbnails = thumbnailsList.querySelectorAll('img');
	let currentIndex = 1; // Изменили начальное значение на 1

	function setActiveItem(newIndex) {
		thumbnails.forEach((thumbnail, index) => {
			thumbnail.classList.remove('active', 'left', 'right');
			if (index === newIndex) {
				thumbnail.classList.add('active');
			} else if (index === newIndex - 1 || (newIndex === 0 && index === thumbnails.length - 1)) {
				thumbnail.classList.add('left');
			} else if (index === newIndex + 1 || (newIndex === thumbnails.length - 1 && index === 0)) {
				thumbnail.classList.add('right');
			}
		});

		const mainImage = document.querySelector('.main-image img');
		mainImage.src = thumbnails[newIndex].src;
		mainImage.alt = thumbnails[newIndex].alt;
	}

	thumbnails.forEach((thumbnail, index) => {
		thumbnail.addEventListener('click', function () {
			const newIndex = Array.from(thumbnails).indexOf(thumbnail);

			if (newIndex !== currentIndex) {
				setActiveItem(newIndex);
				currentIndex = newIndex;
			}
		});
	});

	// Установка активной миниатюры второй по порядку
	setActiveItem(1);
});



document.addEventListener('DOMContentLoaded', function () {


	// =============
	// burdger
	// =============

	var navIcon = document.getElementById('nav-icon1');
	var menuBox = document.getElementById('menubox');

	navIcon.addEventListener('click', function () {
		navIcon.classList.toggle('open');
		menuBox.classList.toggle('open');
	});




});