import define1 from "./450051d7f1174df8@254.js";

function _1(md){return(
md`# Cryptopunks Project Vis Development
`
)}

function _data(FileAttachment){return(
FileAttachment("pipeline.csv").csv({typed: true})
)}

function _orders_data(FileAttachment){return(
FileAttachment("orders.csv").csv({typed: true})
)}

function _gains_data(FileAttachment){return(
FileAttachment("gains.csv").csv({typed: true})
)}

function _x(d3,data,margin,width){return(
d3.scaleUtc()
    .domain(d3.extent(data, d => d.TradeDate))
    .range([margin.left, width - margin.right])
)}

function _y(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([0, d3.max(data, d => d.bollinger_band_upper)])
    .range([height - margin.bottom, margin.top])
)}

function _12(md){return(
md`<b>Interactive component: Select viewing window`
)}

function _timeframe(Inputs){return(
Inputs.radio(new Map([
  ["All",  [new Date("2017-01-01"), new Date("2023-01-01")]],
  ["2017", [new Date("2017-01-01"), new Date("2018-01-01")]],
  ["2018", [new Date("2018-01-01"), new Date("2019-01-01")]],
  ["2019", [new Date("2019-01-01"), new Date("2020-01-01")]],
  ["2020", [new Date("2020-01-01"), new Date("2021-01-01")]],
  ["2021", [new Date("2021-01-01"), new Date("2022-01-01")]],
  ["2022", [new Date("2022-01-01"), new Date("2023-01-01")]]
]), {key: "All"})
)}

function _chart(d3,width,height,x,y,data,xAxis,yAxis)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x.copy(); // x, but with a new domain.


  // ADD LINES HERE 
  const line1 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => y(d.Low));

  const line2 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => y(d.High));

  const line3 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => y(d.bollinger_sma));

  //AND PATH FOR EACH LINE AND SET ITS ATTRIBUTES
  const path1 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line1(data));

  const path2 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line2(data));
  
  const path3 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line3(data));
  
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

function _16(md){return(
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
  const fileAttachments = new Map([["gains.csv",new URL("./files/6617e96713e45b295e85c031148402d1b4765af40df0be95d7c49215cdde0f78fe50bc79aa16476af094c8f7968560e5a64b88376264355bd744c03e87afcec0",import.meta.url)],["orders.csv",new URL("./files/d86e1a00c3fb63076884707fc2d81f21158e15b1b377db66d123f642e05d93e984e477a52d776cc8e068ac75db181a6c67ba8c11b957cba818006ecb64d87fc0",import.meta.url)],["pipeline.csv",new URL("./files/d6a0d27cf5fe7fce3ad195b1b5511073be97593cbe1540262845e87ac114bcf697e819be87db3bc5de08681e67415991b0a4258c6092b3ecce87adca338eef41",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("data")).define("data", ["FileAttachment"], _data);
  main.variable(observer("orders_data")).define("orders_data", ["FileAttachment"], _orders_data);
  main.variable(observer("gains_data")).define("gains_data", ["FileAttachment"], _gains_data);
  main.variable(observer("x")).define("x", ["d3","data","margin","width"], _x);
  main.variable(observer("y")).define("y", ["d3","data","height","margin"], _y);
  main.variable(observer()).define(["md"], _12);
  main.variable(observer("viewof timeframe")).define("viewof timeframe", ["Inputs"], _timeframe);
  main.variable(observer("timeframe")).define("timeframe", ["Generators", "viewof timeframe"], (G, _) => G.input(_));
  main.variable(observer("chart")).define("chart", ["d3","width","height","x","y","data","xAxis","yAxis"], _chart);
  main.variable(observer("update")).define("update", ["chart","timeframe"], _update);
  main.variable(observer()).define(["md"], _16);
  main.variable(observer("xAxis")).define("xAxis", ["x","height","margin","d3","width"], _xAxis);
  main.variable(observer("yAxis")).define("yAxis", ["margin","d3","y","height"], _yAxis);
  main.variable(observer("height")).define("height", _height);
  main.variable(observer("margin")).define("margin", _margin);
  const child1 = runtime.module(define1);
  main.import("Scrubber", child1);
  return main;
}
