async function getWeather() {
  const city = document.getElementById("cityInput").value;
  const res = await fetch(`/api/weather?city=${city}`);
  const data = await res.json();
  const resultDiv = document.getElementById("result");

  if (res.ok) {
    resultDiv.innerHTML = `🌤 ${data.city}: ${data.temperature}°C, ${data.condition}`;
  } else {
    resultDiv.innerHTML = `❌ Error: ${data}`;
  }
}
