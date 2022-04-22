// https://observablehq.com/@sssantos/cryptopunks-project-vis-development@1618
function _1(md){return(
md`# Cryptopunks Project Vis Development
`
)}

function _params(){return(
{
"ticker": "BTC",
"training_sd": "2017-05-01", //mandatory
"training_ed": "2018-05-01",
"test_sd": "2018-05-02",
"test_ed": "2019-02-01",
"sv": 500000,
"sma_window": 14,
"bollinger_window": 14,
"bollinger_stdvs": 3,
"so_window": 14,
"so_window_sma": 14,
"obv": true,
"macd": true,
"include_sentiment": true,
"mom_window": 14,
"alpha": 0.1,
"gamma": 0.9,
"rar": 0.99,
"radr": 0.8,
"sma_threshold": 0.2,
"so_ul": 80,
"so_ll": 20,
"mom_threshold": 0.2,
"sentiment_threshold": 0.3
}
)}

function _include_params(Inputs){return(
Inputs.toggle({label: "Include Sentiment Analysis"})
)}

function _4(params,include_params){return(
params['include_sentiment'] = include_params
)}

function _queryString(params){return(
Object.keys(params).map(function(key) {
return key + '=' + params[key]
}).join('&')
)}

function _url(queryString){return(
"http://127.0.0.1:5001/run_qlearner?" + queryString
)}

function _dataset2(url){return(
fetch(url)
    .then(response => response.json())
    .then(function(data) {
        return data

    })
)}

function _cleanedData(dataset2){return(
dataset2.map(d => ({
  'bollinger_band_upper': parseFloat(d.bollinger_band_upper),
  'bollinger_band_lower': parseFloat(d.bollinger_band_lower),
  'TradeDate': new Date(d.TradeDate),
  'rolling_avg': parseFloat(d.rolling_avg)
}))
)}

function _data(cleanedData){return(
cleanedData
)}

function _orders_data(FileAttachment){return(
FileAttachment("orders.csv").csv({typed: true})
)}

function _x(d3,data,margin,width){return(
d3.scaleUtc()
    .domain(d3.extent(data, d => d.TradeDate))
    .range([margin.left, width - margin.right])
)}

function _y(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([0, d3.max(data, d => +d.bollinger_band_upper)])
    .range([height - margin.bottom, margin.top])
)}

function _13(md){return(
md`<b>Select viewing window`
)}

function _timeframe(Inputs){return(
Inputs.radio(new Map([
  ["All",  [new Date("2017-01-01"), new Date("2020-01-01")]],
  ["2017", [new Date("2017-01-01"), new Date("2018-01-01")]],
  ["2018", [new Date("2018-01-01"), new Date("2019-01-01")]],
  ["2019", [new Date("2019-01-01"), new Date("2020-01-01")]],
//   ["2020", [new Date("2020-01-01"), new Date("2021-01-01")]],
//   ["2021", [new Date("2021-01-01"), new Date("2022-01-01")]],
//   ["2022", [new Date("2022-01-01"), new Date("2023-01-01")]]
]), {key: "All"})
)}

function _include1(Inputs){return(
Inputs.toggle({label: "Bollinger Upper"})
)}

function _include2(Inputs){return(
Inputs.toggle({label: "Bollinger Band Lower"})
)}

function _include3(Inputs){return(
Inputs.toggle({label: "Bollinger SMA"})
)}

function _18(htl){return(
htl.html`     <pre>     <h1>  Bollinger Band Graph </pre>`
)}

function _chart(d3,width,height,x,include1,y,data,include2,include3,xAxis,yAxis)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x.copy(); // x, but with a new domain.

  var line1 = d3.line()
  var path1 = svg.append("path")
  if (include1 == 1) {
    line1 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => y(+d.bollinger_band_upper));

    path1 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line1(data));
  }


  var line2 = d3.line()
  var path2 = svg.append("path")
  if (include2 == 1) {
    line2 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => y(+d.bollinger_band_lower));

    path2 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line2(data));
  }

  var line3 = d3.line()
  var path3 = svg.append("path")
  if (include3 == 1) {
    line3 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => y(+d.rolling_avg));

    path3 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line3(data));
  }
  
  // const line2 = d3.line()
  //     .x(d => zx(d.TradeDate))
  //     .y(d => y(+d.rolling_avg));

  // const path2 = svg.append("path")
  //   .attr("fill", "none")
  //   .attr("stroke", "red")
  //   .attr("stroke-width", 1)
  //   .attr("stroke-miterlimit", 1)
  //   .attr("d", line2(data));
  
  // const line3 = d3.line()
  //     .x(d => zx(d.TradeDate))
  //     .y(d => y(+d.bollinger_band_lower));

  // const path3 = svg.append("path")
  //     .attr("fill", "none")
  //     .attr("stroke", "purple")
  //     .attr("stroke-width", 1)
  //     .attr("stroke-miterlimit", 1)
  //     .attr("d", line3(data));
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis, y);

  return Object.assign(svg.node(), {
    update(domain) {
      const t = svg.transition().duration(750);
      zx.domain(domain);
      gx.transition(t).call(xAxis, zx);
      // ADD PATH TRANSITIONS HERE SO THAT THEY SCALE WITH VIEWING WINDOW
      path1.transition(t).attr("d", line1(data));
      path2.transition(t).attr("d", line2(data));
      path3.transition(t).attr("d", line3(data));
    }
  });
}


function _update(chart,timeframe){return(
chart.update(timeframe)
)}

function _21(md){return(
md`---

## Appendix`
)}

function _xAxis(x,height,margin,d3,width){return(
(g, scale = x) => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(scale).ticks(width / 80).tickSizeOuter(0))
)}

function _yAxis(margin,d3,y,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _height(){return(
480
)}

function _margin(){return(
{top: 20, right: 30, bottom: 30, left: 40}
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["orders.csv",new URL("./files/d86e1a00c3fb63076884707fc2d81f21158e15b1b377db66d123f642e05d93e984e477a52d776cc8e068ac75db181a6c67ba8c11b957cba818006ecb64d87fc0",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("params")).define("params", _params);
  main.variable(observer("viewof include_params")).define("viewof include_params", ["Inputs"], _include_params);
  main.variable(observer("include_params")).define("include_params", ["Generators", "viewof include_params"], (G, _) => G.input(_));
  main.variable(observer()).define(["params","include_params"], _4);
  main.variable(observer("queryString")).define("queryString", ["params"], _queryString);
  main.variable(observer("url")).define("url", ["queryString"], _url);
  main.variable(observer("dataset2")).define("dataset2", ["url"], _dataset2);
  main.variable(observer("cleanedData")).define("cleanedData", ["dataset2"], _cleanedData);
  main.variable(observer("data")).define("data", ["cleanedData"], _data);
  main.variable(observer("orders_data")).define("orders_data", ["FileAttachment"], _orders_data);
  main.variable(observer("x")).define("x", ["d3","data","margin","width"], _x);
  main.variable(observer("y")).define("y", ["d3","data","height","margin"], _y);
  main.variable(observer()).define(["md"], _13);
  main.variable(observer("viewof timeframe")).define("viewof timeframe", ["Inputs"], _timeframe);
  main.variable(observer("timeframe")).define("timeframe", ["Generators", "viewof timeframe"], (G, _) => G.input(_));
  main.variable(observer("viewof include1")).define("viewof include1", ["Inputs"], _include1);
  main.variable(observer("include1")).define("include1", ["Generators", "viewof include1"], (G, _) => G.input(_));
  main.variable(observer("viewof include2")).define("viewof include2", ["Inputs"], _include2);
  main.variable(observer("include2")).define("include2", ["Generators", "viewof include2"], (G, _) => G.input(_));
  main.variable(observer("viewof include3")).define("viewof include3", ["Inputs"], _include3);
  main.variable(observer("include3")).define("include3", ["Generators", "viewof include3"], (G, _) => G.input(_));
  main.variable(observer()).define(["htl"], _18);
  main.variable(observer("chart")).define("chart", ["d3","width","height","x","include1","y","data","include2","include3","xAxis","yAxis"], _chart);
  main.variable(observer("update")).define("update", ["chart","timeframe"], _update);
  main.variable(observer()).define(["md"], _21);
  main.variable(observer("xAxis")).define("xAxis", ["x","height","margin","d3","width"], _xAxis);
  main.variable(observer("yAxis")).define("yAxis", ["margin","d3","y","height"], _yAxis);
  main.variable(observer("height")).define("height", _height);
  main.variable(observer("margin")).define("margin", _margin);
  return main;
}
