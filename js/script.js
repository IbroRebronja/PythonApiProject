document.getElementById("getWeather").addEventListener("click", () => {
    const city = document.getElementById("cityInput").value.trim();

    if (!city) {
        document.getElementById("weatherResult").innerHTML = `<p>Please enter a city.</p>`;
        return;
    }

    fetch(`http://localhost:8000/api/weather?city=${city}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("weatherResult").innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                document.getElementById("weatherResult").innerHTML = `
                    <h2>${data.name}, ${data.sys.country}</h2>
                    <p>Temperature: ${data.main.temp}°C</p>
                    <p>Weather: ${data.weather[0].description}</p>
                    <p>Humidity: ${data.main.humidity}%</p>
                    <p>Wind Speed: ${data.wind.speed} m/s</p>
                `;
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
            document.getElementById("weatherResult").innerHTML = `<p>Failed to fetch data.</p>`;
        });
});
