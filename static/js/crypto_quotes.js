document.addEventListener("DOMContentLoaded", function () {
  console.log("crypto_quotes.js loaded");

  const cryptoSymbol = Array.from(document.querySelectorAll("#symbols")).map(
    (element) => element.textContent
  );

  const getColorClass = (value) => {
    if (value > 0) return "text-success";
    if (value < 0) return "text-danger";
    return "text-secondary";
  };

  cryptoSymbol.forEach((symbol) => {
    const formattedSymbol = `BINANCE:${symbol}`;
    const cryptoSocket = new WebSocket(
      `ws://${window.location.host}/ws/crypto/${formattedSymbol}/`
    );

    // 📦 Cache cell references only once
    const cellRefs = {
      c: document.querySelector(`td#c[data-symbol="${symbol}"]`),
      d: document.querySelector(`td#d[data-symbol="${symbol}"]`),
      dp: document.querySelector(`td#dp[data-symbol="${symbol}"]`),
      h: document.querySelector(`td#h[data-symbol="${symbol}"]`),
      l: document.querySelector(`td#l[data-symbol="${symbol}"]`),
      o: document.querySelector(`td#o[data-symbol="${symbol}"]`),
      pc: document.querySelector(`td#pc[data-symbol="${symbol}"]`),
      t: document.querySelector(`td#t[data-symbol="${symbol}"]`),
    };

    if (!cellRefs.c) {
      console.warn(`Missing element for symbol: ${symbol}`);
      return;
    }

    cryptoSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      console.log("WebSocket Data Received:", data, new Date());

      const symbolData = data[formattedSymbol];
      if (!symbolData) return;

      const {
        c: currentPrice,
        d: change,
        dp: changePercent,
        h: highPrice,
        l: lowPrice,
        o: openPrice,
        pc: previousClosePrice,
        t: time,
      } = symbolData;

      // Check that cellRefs exist and log before update
      console.log("Cell references for symbol", symbol, cellRefs);

      if (cellRefs.c) {
        console.log(
          `Updating current price for ${symbol}: $${
            currentPrice?.toFixed(2) || "-"
          }`
        );
        cellRefs.c.textContent = `$${currentPrice?.toFixed(2) || "-"}`;
      }

      if (cellRefs.d) {
        console.log(
          `Updating change for ${symbol}: ${change?.toFixed(2) || "-"}`
        );
        cellRefs.d.textContent = change?.toFixed(2) || "-";
        cellRefs.d.className = getColorClass(change);
      }

      if (cellRefs.dp) {
        console.log(
          `Updating change percentage for ${symbol}: ${changePercent?.toFixed(
            2
          )}%`
        );
        cellRefs.dp.textContent = changePercent
          ? `${changePercent.toFixed(2)}%`
          : "-";
        cellRefs.dp.className = getColorClass(changePercent);
      }

      // Same for other fields...
      if (cellRefs.h)
        cellRefs.h.textContent = `$${highPrice?.toFixed(3) || "-"}`;
      if (cellRefs.l)
        cellRefs.l.textContent = `$${lowPrice?.toFixed(3) || "-"}`;
      if (cellRefs.o)
        cellRefs.o.textContent = `$${openPrice?.toFixed(3) || "-"}`;
      if (cellRefs.pc)
        cellRefs.pc.textContent = `$${previousClosePrice?.toFixed(3) || "-"}`;

      if (cellRefs.t) {
        const formattedTime = new Date(time * 1000).toLocaleString("en-US", {
          timeZone: "Asia/Dhaka",
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        });
        console.log(`Updating time for ${symbol}: ${formattedTime}`);
        cellRefs.t.textContent = formattedTime;
      }
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
