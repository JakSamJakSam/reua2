function changeImage(imageSrc) {
	const mainImage = document.querySelector('.single__wrapper .main-image img');
	mainImage.src = imageSrc;
	mainImage.alt = imageSrc;
}



document.addEventListener('DOMContentLoaded', function () {
	const thumbnailsList = document.querySelector('.thumbnails-list');
	const thumbnails = thumbnailsList.querySelectorAll('img');
	let currentIndex = 2;

	function setActiveItem(newIndex) {
		thumbnails.forEach((thumbnail, index) => {
			thumbnail.classList.remove('active', 'left', 'right', 'center');
			if (index === newIndex) {
				thumbnail.classList.add('active');
			} else if (index === (newIndex + 1) % thumbnails.length) {
				thumbnail.classList.add('center');
			} else if (index === (newIndex - 1 + thumbnails.length) % thumbnails.length) {
				thumbnail.classList.add('left');
			} else if (index === (newIndex + 2) % thumbnails.length) {
				thumbnail.classList.add('right');
			}
		});

		const mainImage = document.querySelector('.main-image img');
		mainImage.src = thumbnails[newIndex].src;
		mainImage.alt = thumbnails[newIndex].alt;
	}

	thumbnails.forEach((thumbnail, index) => {
		thumbnail.addEventListener('click', function () {
			const newIndex = parseInt(thumbnail.getAttribute('data-index'));

			if (newIndex !== currentIndex) {
				setActiveItem(newIndex);
				currentIndex = newIndex;
			}
		});
	});

	document.getElementById('right').addEventListener('click', function () {
		currentIndex = (currentIndex + 1) % thumbnails.length;
		setActiveItem(currentIndex);
	});

	document.getElementById('left').addEventListener('click', function () {
		currentIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
		setActiveItem(currentIndex);
	});

	// Set active thumbnail initially
	setActiveItem(currentIndex);
});
