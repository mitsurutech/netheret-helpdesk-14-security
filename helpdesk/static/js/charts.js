// Draws a bar chart above every table with class "chart".
// The labels come from the first column and the numbers from the second,
// so the table and the chart always show the same data.

function drawChart(table) {
  var rows = table.querySelectorAll("tbody tr");
  var labels = [];
  var values = [];
  rows.forEach(function (row) {
    labels.push(row.cells[0].textContent.trim());
    values.push(parseFloat(row.cells[1].textContent) || 0);
  });
  if (values.length === 0) {
    return;
  }
  var unit = table.dataset.unit || "";

  // Read the colours from the CSS, so the chart matches the page.
  var style = getComputedStyle(document.documentElement);
  var barColour = style.getPropertyValue("--chart-bar").trim();
  var textColour = style.getPropertyValue("--ink").trim();

  var barHeight = 28;
  var gap = 10;
  var labelWidth = 220;
  var width = Math.min(table.parentElement.clientWidth, 700);
  var height = values.length * (barHeight + gap) + gap;

  var canvas = document.createElement("canvas");
  // The chart is a picture of the table, so screen readers skip it and
  // read the table instead.
  canvas.setAttribute("aria-hidden", "true");
  // Draw at the screen's real pixel density so the text is sharp.
  var scale = window.devicePixelRatio || 1;
  canvas.width = width * scale;
  canvas.height = height * scale;
  canvas.style.width = width + "px";
  canvas.style.height = height + "px";
  var ctx = canvas.getContext("2d");
  ctx.scale(scale, scale);

  var biggest = Math.max.apply(null, values) || 1;
  var fontSize = parseFloat(getComputedStyle(document.body).fontSize) || 16;
  ctx.font = Math.round(fontSize * 0.9) + "px sans-serif";
  ctx.textBaseline = "middle";

  // Leave room on the right for the number after the longest bar.
  var room = width - labelWidth - 60;
  values.forEach(function (value, i) {
    var y = gap + i * (barHeight + gap);
    var barWidth = Math.max(2, (value / biggest) * room);

    ctx.fillStyle = textColour;
    ctx.textAlign = "right";
    var label = labels[i].length > 28 ? labels[i].slice(0, 27) + "…" : labels[i];
    ctx.fillText(label, labelWidth - 10, y + barHeight / 2);

    ctx.fillStyle = barColour;
    ctx.fillRect(labelWidth, y, barWidth, barHeight);

    ctx.fillStyle = textColour;
    ctx.textAlign = "left";
    ctx.fillText(value + unit, labelWidth + barWidth + 6, y + barHeight / 2);
  });

  table.parentElement.insertBefore(canvas, table);
}

document.querySelectorAll("table.chart").forEach(drawChart);
