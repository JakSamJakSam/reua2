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


	// =============
	// burdger
	// =============

	var navIcon = document.getElementById('nav-icon1');
	var menuBox = document.getElementById('menubox');

	navIcon.addEventListener('click', function () {
		navIcon.classList.toggle('open');
		menuBox.classList.toggle('open');
	});


	// =============
	// scroll to id
	// =============

	document.querySelectorAll(".to_id").forEach(function (element) {
		element.addEventListener("click", function (e) {
			e.preventDefault();
			document.querySelector("#menuToggle input[type='checkbox']").checked = false;
		});
	});

	const anchors = document.querySelectorAll('a[href*="#"]');
	for (let anchor of anchors) {
		anchor.addEventListener('click', function (e) {
			e.preventDefault();
			const blockID = anchor.getAttribute('href').substr(1);
			const targetElement = document.getElementById(blockID);
			if (targetElement) {
				const anchorPosition = targetElement.getBoundingClientRect().top + window.scrollY;
				window.scrollTo({
					top: anchorPosition - 100,
					behavior: 'smooth'
				});
			}
		});
	}


	// =============
	// Modal
	// =============

	const openModalButton = document.getElementById("openVideoModal");
	const modal = document.getElementById("video__modal");
	const closeModalButton = document.getElementById("close__modal");
	const closeModalBG = document.getElementById("bg__modal");
	const videoPlayer = document.getElementById("video__player");

	// Функция для воспроизведения видео и открытия модального окна
	function openModal() {
		modal.style.display = "block";
		videoPlayer.play();
	}

	// Функция для паузы видео и закрытия модального окна
	function closeModal() {
		modal.style.display = "none";
		videoPlayer.pause();
	}

	// Обработчики событий
	openModalButton.addEventListener("click", openModal);
	closeModalButton.addEventListener("click", closeModal);
	closeModalBG.addEventListener("click", closeModal);

	// Закрытие модального окна при клике за его пределами
	window.addEventListener("click", function (event) {
		if (event.target === modal) {
			closeModal();
		}
	});




	// =============
	// projects slider
	// =============

	if (document.documentElement.clientWidth > 1000) {
		const sliderContainer = document.querySelector("#projects .item__wrapper");
		const prevButton = document.querySelector(".prev-button");
		const nextButton = document.querySelector(".next-button");

		const slideWidth = sliderContainer.clientWidth / 3; // Изменено на / 3
		let currentIndex = 0;

		nextButton.addEventListener("click", () => {
			currentIndex = (currentIndex + 1) % 5;
			updateSlider();
		});

		prevButton.addEventListener("click", () => {
			currentIndex = (currentIndex - 1 + 5) % 5;
			updateSlider();
		});

		function updateSlider() {
			const offsetX = -currentIndex * slideWidth;
			sliderContainer.style.transform = `translateX(${offsetX}px)`;
		}

		updateSlider();
	} else {
		const sliderContainer = document.querySelector("#projects .item__wrapper");
		const prevButton = document.querySelector(".prev-button");
		const nextButton = document.querySelector(".next-button");

		const slideWidth = sliderContainer.clientWidth;
		let currentIndex = 0;

		nextButton.addEventListener("click", () => {
			currentIndex = (currentIndex + 1) % 7;
			updateSlider();
		});

		prevButton.addEventListener("click", () => {
			currentIndex = (currentIndex - 1 + 7) % 7;
			updateSlider();
		});

		function updateSlider() {
			const offsetX = -currentIndex * slideWidth;
			sliderContainer.style.transform = `translateX(${offsetX}px)`;
		}

		updateSlider();

	}


	// =============
	// scroll animation
	// =============

	if (document.documentElement.clientWidth > 1200) {
		// Функция, которая будет выполняться при прокрутке страницы
		function handleScroll() {
			const blocks = document.querySelectorAll(".scroll_animation");
			blocks.forEach(block => {
				if (isElementInViewport(block, 0.65)) { // 0.1 - процент видимости
					block.classList.add("visible");
					block.classList.remove("hidden");
				}
			});
		}

		// Функция для проверки, виден ли элемент на экране с определенным порогом видимости (в примере 0.1 - 10%)
		function isElementInViewport(el, threshold) {
			const rect = el.getBoundingClientRect();
			const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
			const height = rect.bottom - rect.top;
			return (rect.top >= -height * threshold && rect.bottom <= viewportHeight + height * threshold);
		}

		// Добавляем слушатель события прокрутки страницы
		window.addEventListener("scroll", handleScroll);

		// Первичная проверка при загрузке страницы
		handleScroll();


		// =============
		// scroll animation .title__inner 
		// =============

		// JavaScript для керування margin - left в залежності від прокрутки
		window.addEventListener("scroll", function () {
			const titleInner = document.querySelector(".title__inner");
			const scrollY = window.scrollY;
			const maxMargin = 15; // Максимальне значення margin-left у vw

			// Визначаємо нове значення margin-left в залежності від прокрутки
			const newMargin = Math.min(maxMargin, scrollY / 100); // Змінюйте 100, щоб налаштувати швидкість зсуву

			titleInner.style.marginLeft = `${newMargin}vw`;
		});
	}


	// =============
	// video slider
	// =============

	const slider = document.querySelector('.slider');
	const items = document.querySelectorAll('.slider__item');
	const arrowNext = document.querySelector('.arrow_prew');
	const arrowPrew = document.querySelector('.arrow__next');

	// Функция для установки активного элемента и управления видео
	function setActiveItem(newActiveIndex) {
		items.forEach((item, index) => {
			item.classList.remove('active', 'left', 'right');
			const video = item.querySelector('video');
			if (video) {
				video.pause();
				video.removeAttribute('autoplay');
				video.removeAttribute('controls');
				video.removeAttribute('muted');
			}
			if (index === newActiveIndex) {
				item.classList.add('active');
				const activeVideo = item.querySelector('video');
				if (activeVideo) {
					activeVideo.play();
					activeVideo.setAttribute('autoplay', '');
					activeVideo.setAttribute('controls', '');
					activeVideo.setAttribute('muted', '');
				}
			} else if (index === newActiveIndex - 1) {
				item.classList.add('right');
			} else if (index === newActiveIndex + 1) {
				item.classList.add('left');
			}
		});
	}

	// Обработчик нажатия на стрелку влево
	arrowPrew.addEventListener('click', () => {
		const currentActiveIndex = Array.from(items).findIndex(item => item.classList.contains('active'));
		if (currentActiveIndex > 0) {
			setActiveItem(currentActiveIndex - 1);
		} else {
			arrowPrew.classList.add('disabled');
		}
	});

	// Обработчик нажатия на стрелку вправо
	arrowNext.addEventListener('click', () => {
		const currentActiveIndex = Array.from(items).findIndex(item => item.classList.contains('active'));
		if (currentActiveIndex < items.length - 1) {
			setActiveItem(currentActiveIndex + 1);
		}
	});


	// =============
	// map
	// =============

	const buttonNeeded = document.querySelector('.button__needed');
	const buttonAvailable = document.querySelector('.button__available');
	const amountReH20 = document.querySelector('.amount p');
	const amount = document.querySelector('.amount');
	const regionsNeeded = {
		ZaporizhiaRegion: document.getElementById("zaporizhia_region"),
		ChernihivRegion: document.getElementById("chernihiv_region"),
		SumyRegion: document.getElementById("sumy_region"),
		PoltavaRegion: document.getElementById("poltava_region"),
		KirovohradRegion: document.getElementById("kirovohrad_region"),
		MykolaivRegion: document.getElementById("mykolaiv_region"),
		KhersonRegion: document.getElementById("kherson_region"),
	};
	buttonNeeded.addEventListener('click', () => {
		buttonNeeded.classList.add('not__active');
		buttonNeeded.classList.remove('active');
		buttonAvailable.classList.add('active');
		buttonAvailable.classList.remove('not__active');
		amount.classList.remove('hidden');
		for (const key in regionsNeeded) {
			regionsNeeded[key].classList.add('active');
		}
	})

	buttonAvailable.addEventListener('click', () => {
		buttonAvailable.classList.add('not__active');
		buttonAvailable.classList.remove('active');
		buttonNeeded.classList.add('active');
		buttonNeeded.classList.remove('not__active');
		amount.classList.add('hidden');
		for (const key in regionsNeeded) {
			regionsNeeded[key].classList.remove('active');
		}
	})

	var phoneInput = document.getElementById("id_phone");

	phoneInput.addEventListener("input", function () {
		var value = phoneInput.value.replace(/\D/g, '');

		if (value.length > 10) {
			value = value.slice(0, 12);
		}

		if (value.length === 1 && value !== '3' && value !== '8') {
			value = '38' + value;
		}
		if (value.length > 1 && value.length <= 12) {
			value = '+38(' + value.substring(2, 5) + ')' + value.substring(5, 8) + '-' + value.substring(8);
		}

		phoneInput.value = value;
	});

});


