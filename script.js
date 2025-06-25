async function getWeather() {
  const city = document.getElementById("cityInput").value;
  try {
    const res = await fetch(`/api/weather?city=${city}`);
    const text = await res.text();

    const data = JSON.parse(text);
    if (res.ok) {
      document.getElementById("result").innerText =
        `🌤 ${data.city}: ${data.temperature}°C, ${data.condition}`;
    } else {
      document.getElementById("result").innerText =
        `❌ Error: ${data.error || 'Something went wrong'}`;
    }
  } catch (err) {
    document.getElementById("result").innerText = "⚠️ Failed to fetch weather.";
    console.error("Parse or fetch error:", err);
  }
}
