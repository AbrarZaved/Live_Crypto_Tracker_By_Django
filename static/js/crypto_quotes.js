document.addEventListener("DOMContentLoaded", function () {
  console.log("crypto_quotes.js loaded");

  const roomName = JSON.parse(document.getElementById("room-name").textContent);
  const cryptoSymbol = Array.from(document.querySelectorAll("#symbols")).map(
    (element) => element.textContent
  );
  console.log(cryptoSymbol);
  cryptoSymbol.forEach((symbol) => {
    const formattedSymbol = `BINANCE:${symbol}`;
    const cryptoSocket = new WebSocket(
      `ws://${window.location.host}/ws/crypto/${formattedSymbol}/`
    );

    cryptoSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);

      // If backend sends a single object per symbol, use data directly.
      const {
        c: currentPrice,
        d: change,
        dp: changePercent,
        h: highPrice,
        l: lowPrice,
        o: openPrice,
        pc: previousClosePrice,
        t: time,
      } = data;
      const getColorClass = (value) => {
        if (value > 0) return "text-success";
        if (value < 0) return "text-danger";
        return "text-secondary";
      };
      // Select the correct row by symbol using data-symbol attribute
      const symbolId = symbol; // already without BINANCE:
      const updateCell = (id) =>
        document.querySelector(`td#${id}[data-symbol="${symbolId}"]`);

      updateCell("c").textContent = `$${currentPrice?.toFixed(2) || "-"}`;
      const dCell = updateCell("d");
      dCell.textContent = change?.toFixed(2) || "-";
      dCell.className = getColorClass(change);
      const dpCell = updateCell("dp");
      dpCell.textContent = changePercent ? `${changePercent.toFixed(2)}%` : "-";
      dpCell.className = getColorClass(changePercent);
      updateCell("h").textContent = `$${highPrice?.toFixed(3) || "-"}`;
      updateCell("l").textContent = `$${lowPrice?.toFixed(3) || "-"}`;
      updateCell("o").textContent = `$${openPrice?.toFixed(3) || "-"}`;
      updateCell("pc").textContent = `$${
        previousClosePrice?.toFixed(3) || "-"
      }`;
      updateCell("t").textContent = new Date(time * 1000).toLocaleString(
        "en-US",
        {
          timeZone: "Asia/Dhaka",
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        }
      );
    };

    cryptoSocket.onopen = () => {
      console.log(`WebSocket opened for ${formattedSymbol}`);
    };

    cryptoSocket.onerror = (error) => {
      console.error(`WebSocket error for ${formattedSymbol}:`, error);
    };

    cryptoSocket.onclose = (event) => {
      console.warn(`WebSocket closed for ${formattedSymbol}:`, event);
    };
  });
});
