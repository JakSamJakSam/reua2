/**
 * Ставит точку на SVG-карту Украины (формата SimpleMaps / Wikipedia) по широте и долготе
 * @param {SVGElement} svgElement - DOM-элемент <svg>
 * @param {number} lat - Широта (например, 50.4501)
 * @param {number} lon - Долгота (например, 30.5234)
 * @param {Object} options - Настройки внешнего вида точки
 */
function addPointToUkraineMap(svgElement, lat, lon, options = {}) {
  const {
    color = '#ff3b30',
    radius = 5,
    stroke = '#ffffff',
    strokeWidth = 1.5,
    label = ''
  } = options;

  // 1. Откалиброванные географические границы с учетом внутренних полей холста
  const BOUNDS = {
    minLon: 22.02,  // Левый край холста (чуть западнее Закарпатья)
    maxLon: 40.35,  // Правый край холста (чуть восточнее Луганской обл.)
    maxLat: 52.44,  // Верхний край холста (чуть севернее Черниговской обл.)
    minLat: 44.30   // Нижний край холста (чуть южнее мыса Сарыч в Крыму)
  };

  // 2. Получаем размеры координатной сетки SVG
  const viewBox = svgElement.viewBox.baseVal;
  const width = (viewBox && viewBox.width) || parseFloat(svgElement.getAttribute('width')) || 1000;
  const height = (viewBox && viewBox.height) || parseFloat(svgElement.getAttribute('height')) || 674;

  // 3. Расчет X (линейно по долготе)
  const x = ((lon - BOUNDS.minLon) / (BOUNDS.maxLon - BOUNDS.minLon)) * width;

  // 4. Расчет Y (по проекции Меркатора, чтобы точки в центре не съезжали по вертикали)
  const toMercatorY = (latitude) => {
    const rad = (latitude * Math.PI) / 180;
    return Math.log(Math.tan(Math.PI / 4 + rad / 2));
  };

  const mercMinY = toMercatorY(BOUNDS.minLat);
  const mercMaxY = toMercatorY(BOUNDS.maxLat);
  const mercY = toMercatorY(lat);

  const y = ((mercMaxY - mercY) / (mercMaxY - mercMinY)) * height;

  // 5. Отрисовка точки (и подписи, если передана)
  const svgNS = 'http://www.w3.org/2000/svg';
  const group = document.createElementNS(svgNS, 'g');

  const circle = document.createElementNS(svgNS, 'circle');
  circle.setAttribute('cx', x.toFixed(2));
  circle.setAttribute('cy', y.toFixed(2));
  circle.setAttribute('r', radius);
  circle.setAttribute('fill', color);
  circle.setAttribute('stroke', stroke);
  circle.setAttribute('stroke-width', strokeWidth);
  group.appendChild(circle);

  if (label) {
    const text = document.createElementNS(svgNS, 'text');
    text.setAttribute('x', (x + radius + 4).toFixed(2));
    text.setAttribute('y', (y + 4).toFixed(2));
    text.setAttribute('font-family', 'sans-serif');
    text.setAttribute('font-size', '12');
    text.setAttribute('fill', '#ffffff');
    text.textContent = label;
    group.appendChild(text);
  }

  svgElement.appendChild(group);
  return group;
}



/***
 Роман, привіт!

кидаю адреси для перевірки роботи карти

Донецька обл, Краматорський р-н, селище Олександрівка, вул Центральна 15А

Харків, вулиця Озерянська, буд 5

Сумська область, Конотопський р-н, м. Кролевець, площа Миру, буд 1

Харківська область, м. Лозова, вулиця Ярослава Мудрого, буд 1


Дніпропетровська область, м. Дніпро, вул. Космічна, 21
 **/