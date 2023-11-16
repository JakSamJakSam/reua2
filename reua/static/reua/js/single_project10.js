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
