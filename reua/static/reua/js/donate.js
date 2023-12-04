function toggleActive(btnId, paymentId) {
	// Получаем все кнопки с классом "btn"
	var buttons = document.getElementsByClassName('btn');

	// Удаляем класс "active" у всех кнопок
	for (var i = 0; i < buttons.length; i++) {
		buttons[i].classList.remove('active');
	}

	// Добавляем класс "active" только к выбранной кнопке
	var selectedButton = document.getElementById(btnId);
	selectedButton.classList.add('active');

	// Скрываем все блоки с классом "payment"
	var payments = document.getElementsByClassName('payment');
	for (var i = 0; i < payments.length; i++) {
		payments[i].classList.remove('active');
	}

	// Показываем только активный блок с классом "payment"
	var selectedPayment = document.getElementById(paymentId);
	selectedPayment.classList.add('active');
}