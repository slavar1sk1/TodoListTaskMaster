const particlesContainer = document.querySelector('.particles');

// Массив нежных цветов для частиц
const colors = [
  'rgba(230, 200, 200, 0.6)', // Светло-красный
  'rgba(200, 230, 220, 0.6)', // Светло-зеленый
  'rgba(255, 220, 200, 0.6)', // Светло-оранжевый
  'rgba(200, 220, 255, 0.6)', // Светло-синий
  'rgba(230, 200, 230, 0.6)'  // Светло-пурпурный
];

function createParticle() {
  const particle = document.createElement('div');
  particle.className = 'particle';
  particle.style.left = Math.random() * window.innerWidth + 'px'; // По всей ширине
  particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)]; // Случайный цвет
  particle.style.animationDuration = Math.random() * 4 + 6 + 's'; // Увеличили максимальное время до 10 секунд
  particlesContainer.appendChild(particle);

  // Удаляем частицу после анимации
  particle.addEventListener('animationend', () => {
    particle.remove();
  });
}

// Создаем частицы каждые 150 мс
setInterval(createParticle, 150);
