async function getWeather() {
  const city = document.getElementById("cityInput").value;
  const result = document.getElementById("result");
  try {
    const res = await fetch(`/api/weather?city=${city}`);
    const text = await res.text();
    const data = JSON.parse(text);
    if (res.ok) {
      result.innerText = `🌤 ${data.city}: ${data.temperature}°C, ${data.condition}`;
    } else {
      result.innerText = `❌ ${data.error || 'Unknown error'}`;
    }
  } catch (err) {
    result.innerText = "⚠️ Could not get weather data.";
    console.error("Frontend error:", err);
  }
}
