document.addEventListener("DOMContentLoaded", function () {
  const loading = document.getElementById("loading");
  const select = document.getElementById("stockSelect");

  loading.style.display = "flex";

  fetch("/api/crypto-symbols/")
    .then((res) => res.json())
    .then((data) => {
      data.symbols.forEach((symbol) => {
        const option = document.createElement("option");
        option.value = symbol;
        option.textContent = symbol.replace("BINANCE:", "");
        select.appendChild(option);
      });
      console.log("Load time:", data.load_time);
    })
    .finally(() => {
      loading.style.display = "none";
    });
});
