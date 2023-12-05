// =============
// Modal
// =============

// Общие переменные для всех модальных окон
const modalButtons = document.querySelectorAll(".open-modal");
const closeButtons = document.querySelectorAll(".close");
const modals = document.querySelectorAll(".modal_new");
const videoPlayer = document.getElementById("video__player");

// Функция для открытия модального окна
function openModal(modal) {
	modal.style.display = "block";
	const modalType = modal.getAttribute("data-modal-type");

	if (modalType === "video") {
		videoPlayer.play();
	}
}

// Функция для закрытия модального окна
function closeModal(modal) {
	modal.style.display = "none";
	videoPlayer.pause();
}

// Назначение обработчиков событий для каждой кнопки открытия
modalButtons.forEach(function (button) {
	button.addEventListener("click", function () {
		const modalId = this.getAttribute("data-modal");
		const modal = document.getElementById(modalId);
		openModal(modal);
	});
});

// Назначение обработчиков событий для каждой кнопки закрытия
closeButtons.forEach(function (button) {
	button.addEventListener("click", function () {
		const modalId = this.getAttribute("data-modal");
		const modal = document.getElementById(modalId);
		closeModal(modal);
	});
});

// Закрытие модального окна при клике за его пределами
window.addEventListener("click", function (event) {
	modals.forEach(function (modal) {
		if (event.target === modal) {
			closeModal(modal);
		}
	});
});


// =============
// btn__reh20 - btn__city
// =============


const btnReh20 = document.getElementById('btn__reh20');
const btnCity = document.getElementById('btn__city');
const imgReh20 = document.getElementById('img_reh20');
const imgCity = document.getElementById('img_city');
const paymentReh20 = document.getElementById('payment__reh20');
const paymentCity = document.getElementById('payment__city');

// Функция для изменения классов при нажатии на кнопку "Питна вода"
function handleBtnReh20Click() {
	btnReh20.classList.add('active');
	btnReh20.classList.remove('not__active');

	btnCity.classList.add('not__active');
	btnCity.classList.remove('active');

	imgReh20.classList.remove('active');
	imgCity.classList.add('active');

	paymentReh20.classList.remove('active');
	paymentCity.classList.add('active');
}

// Функция для изменения классов при нажатии на кнопку "Відбудова"
function handleBtnCityClick() {
	btnReh20.classList.add('not__active');
	btnReh20.classList.remove('active');

	btnCity.classList.add('active');
	btnCity.classList.remove('not__active');

	imgReh20.classList.add('active');
	imgCity.classList.remove('active');

	paymentReh20.classList.add('active');
	paymentCity.classList.remove('active');
}

// Назначение обработчиков событий
btnReh20.addEventListener('click', handleBtnCityClick);
btnCity.addEventListener('click', handleBtnReh20Click);














// Назначение обработчика событий для кнопок валюты "Питна вода"
const reh20UahPayment = document.getElementById('reh20__uah__payment');
const reh20UsdPayment = document.getElementById('reh20__usd__payment');
const reh20EurPayment = document.getElementById('reh20__eur__payment');
const reh20GpbPayment = document.getElementById('reh20__gpb__payment');

reh20UahPayment.addEventListener('click', function () {
	activateModal('reh20__uah__modal');
	imgReh20.classList.remove('active');
});

reh20UsdPayment.addEventListener('click', function () {
	activateModal('reh20__usd__modal');
	imgReh20.classList.remove('active');
});

reh20EurPayment.addEventListener('click', function () {
	activateModal('reh20__eur__modal');
	imgReh20.classList.remove('active');
});

reh20GpbPayment.addEventListener('click', function () {
	activateModal('reh20__gpb__modal');
	imgReh20.classList.remove('active');
});

// Назначение обработчика событий для кнопок валюты "Відбудова"
const cityUahPayment = document.getElementById('city__uah__payment');
const cityUsdPayment = document.getElementById('city__usd__payment');
const cityEurPayment = document.getElementById('city__eur__payment');
const cityGpbPayment = document.getElementById('city__gpb__payment');

cityUahPayment.addEventListener('click', function () {
	activateModal('city__uah__modal');
	imgCity.classList.remove('active');
});

cityUsdPayment.addEventListener('click', function () {
	activateModal('city__usd__modal');
	imgCity.classList.remove('active');
});

cityEurPayment.addEventListener('click', function () {
	activateModal('city__eur__modal');
	imgCity.classList.remove('active');
});

cityGpbPayment.addEventListener('click', function () {
	activateModal('city__gpb__modal');
	imgCity.classList.remove('active');
});

// Назначение обработчика событий для кнопки "назад" (back)
document.querySelectorAll('.back').forEach(function (backBtn) {
	backBtn.addEventListener('click', function () {
		const modalId = this.parentElement.id;
		document.getElementById('main__modal').classList.add('active');
		document.getElementById(modalId).classList.remove('active');

		// Возвращаем активные фотографии
		if (modalId.includes('reh2o')) {
			imgReh20.classList.add('active');
		} else if (modalId.includes('city')) {
			imgCity.classList.add('active');
		}
	});
});

// Функция для активации модального блока по его id
function activateModal(modalId) {
	document.getElementById(modalId).classList.add('active');
	document.getElementById('main__modal').classList.remove('active');
}



document.addEventListener('DOMContentLoaded', function () {


	// =============
	// burdger
	// =============
	//
	var navIcon = document.getElementById('nav-icon1');
	var menuBox = document.getElementById('menubox');

	navIcon.addEventListener('click', function () {
		navIcon.classList.toggle('open');
		menuBox.classList.toggle('open');
	});




});
