function _1(md){return(
md`# Cryptopunks Project Vis Development
`
)}

function _include_sentiment(Inputs){return(
Inputs.toggle({value: 0, label: "Include Sentiment"})
)}

function _macd(Inputs){return(
Inputs.toggle({value: 0, label: "MACD"})
)}

function _obv(Inputs){return(
Inputs.toggle({value: 0, label: "On Balance Volume"})
)}

function _alpha(Inputs){return(
Inputs.range([0, 1], {step: 0.01, value: 0.1, label: "Alpha - Learning Rate"})
)}

function _gamma(Inputs){return(
Inputs.range([0, 1], {step: 0.01, value: 0.9, label: "Gamma - Reward Decay Rate"})
)}

function _rar(Inputs){return(
Inputs.range([0, 1], {step: 0.01, value: 0.99, label: "rar - Random Action Rate"})
)}

function _radr(Inputs){return(
Inputs.range([0, 1], {step: 0.01, value: 0.8, label: "radr - Random Action Decay Rate"})
)}

function _smathreshold(Inputs){return(
Inputs.range([0, 0.5], {step: 0.01, value: 0.2, label: "Price to SMA Threshold"})
)}

function _momentumth(Inputs){return(
Inputs.range([0, 0.5], {step: 0.01, value: 0.2, label: "Momentum Threshold"})
)}

function _sentimentth(Inputs){return(
Inputs.range([0, 0.5], {step: 0.01, value: 0.3, label: "Sentiment Threshold"})
)}

function _so_ul(Inputs){return(
Inputs.range([70, 90], {step: 0.01, value: 80, label: "Stochastic Oscillator Upper Limit"})
)}

function _so_ll(Inputs){return(
Inputs.range([10, 30], {step: 0.01, value: 20, label: "Stochastic Oscillator Lower Limit"})
)}

function _training_startdate(Inputs){return(
Inputs.date({value: "2017-05-01", label: "Training Startdate"})
)}

function _training_enddate(Inputs){return(
Inputs.date({value: "2018-05-01", label: "Training Enddate"})
)}

function _testing_startdate(Inputs){return(
Inputs.date({value: "2018-05-02", label: "Testing Startdate"})
)}

function _testing_enddate(Inputs){return(
Inputs.date({value: "2019-02-01", label: "Testing Enddate"})
)}

function _smawindow(Inputs){return(
Inputs.select([7, 14, 21], {value: 14, label: "SMA Window"})
)}

function _bbwindow(Inputs){return(
Inputs.select([7, 14, 21], {value: 14, label: "Bollinger Band Window"})
)}

function _bbstdev(Inputs){return(
Inputs.select([1, 2, 3], {value: 2, label: "Bollinger Band Stdev"})
)}

function _so_window(Inputs){return(
Inputs.select([7, 14, 21], {value: 14,label: "Stochastic Oscillator SMA Window"})
)}

function _so_window_sma(Inputs){return(
Inputs.select([7, 14, 21], {value: 14, label: "Stochastic Oscillator SMA Window"})
)}

function _mom_window(Inputs){return(
Inputs.select([7, 14, 21], {value: 14, label: "Momentum Window"})
)}

function _24(htl){return(
htl.html`     <pre>     <h1>  Run the Q Learner or Grid Search Here </pre>`
)}

function _qlgs(Inputs){return(
Inputs.select(["Run QLearner", "Run GridSearch"], {label: "QLearner or Grid Search:"})
)}

function _rf(Inputs){return(
Inputs.toggle({label: "Fetch Data", value: false})
)}

function _27(htl){return(
htl.html`     <pre>     <h1>  Select viewing window </pre>`
)}

function _dateone(Inputs,training_startdate){return(
Inputs.date({value: training_startdate, label: "StartDate"})
)}

function _datetwo(Inputs,testing_enddate){return(
Inputs.date({value: testing_enddate, label: "EndDate"})
)}

function _30(htl){return(
htl.html`     <pre>     <h1>  Bollinger Band Graph </pre>`
)}

function _inchart1(Inputs){return(
Inputs.toggle({label: "Show Bollinger Graph"})
)}

function _bbg_inputs(Inputs){return(
Inputs.checkbox(["Bollinger Band Upper", "Bollinger Band Lower", "Bollinger SMA", "ADJ Close", "SMA"], {label: "Select Features:"})
)}

function _chart(d3,width,height,x,y,bbg_inputs,data,xAxis,yAxis,inchart1)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x.copy(); // x, but with a new domain.
  const zy = y.copy(); // x, but with a new domain.

  var line1 = d3.line()
  var path1 = svg.append("path")
  if (bbg_inputs.includes("Bollinger Band Upper") == 1) {
    line1 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.bollinger_band_upper));

    path1 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line1(data));
  }
  var line2 = d3.line()
  var path2 = svg.append("path")
  if (bbg_inputs.includes("Bollinger Band Lower") == 1) {
    line2 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.bollinger_band_lower));

    path2 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line2(data));
  }

  var line3 = d3.line()
  var path3 = svg.append("path")
  if (bbg_inputs.includes("Bollinger SMA")) {
    line3 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.bollinger_sma));

    path3 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line3(data));
  }

  var line4 = d3.line()
  var path4 = svg.append("path")
  if (bbg_inputs.includes("ADJ Close")) {
    line4 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.Adj_Close));

    path4 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "green")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line4(data));
  }

  var line5 = d3.line()
  var path5 = svg.append("path")
  if (bbg_inputs.includes("SMA")) {
    line5 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.rolling_avg));

    path5 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "black")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line5(data));
  }
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis, zy);

  if (inchart1){
    return Object.assign(svg.node(), {
      update(domain) {
        const t = svg.transition().duration(750);
        zx.domain(domain);
        gx.transition(t).call(xAxis, zx);
        // ADD PATH TRANSITIONS HERE SO THAT THEY SCALE WITH VIEWING WINDOW
        path1.transition(t).attr("d", line1(data));
        path2.transition(t).attr("d", line2(data));
        path3.transition(t).attr("d", line3(data));
        path4.transition(t).attr("d", line4(data));
        path5.transition(t).attr("d", line5(data));
      }
    });
  }
}


function _34(htl){return(
htl.html`     <pre>     <h1>  Bollinger Percentage </pre>`
)}

function _include6(Inputs){return(
Inputs.toggle({label: "Bollinger Band %"})
)}

function _y2(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([d3.min(data, d => +d.bollinger_band_percentage), d3.max(data, d => +d.bollinger_band_percentage)])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis2(margin,d3,y2,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y2).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _chart2(d3,width,height,x,y2,include6,data,xAxis,yAxis2)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x.copy(); // x, but with a new domain.
  const zy = y2.copy(); // x, but with a new domain.

  var line6 = d3.line()
  var path6 = svg.append("path")
  if (include6 == 1) {
    line6 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.bollinger_band_percentage));

    path6 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line6(data));
  }

  var line62 = d3.line()
  var path62 = svg.append("path")
  if (include6 == 1) {
    line62 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(0));

    path62 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line62(data));
  }

  var line63 = d3.line()
  var path63 = svg.append("path")
  if (include6 == 1) {
    line63 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(1));

    path63 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line63(data));
  }

  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis2, zy);

  if (include6){
    return Object.assign(svg.node(), {
      update(domain) {
        const t = svg.transition().duration(750);
        zx.domain(domain);
        gx.transition(t).call(xAxis, zx);
        // ADD PATH TRANSITIONS HERE SO THAT THEY SCALE WITH VIEWING WINDOW
        path6.transition(t).attr("d", line6(data));
      }
    });
  }
}


function _39(htl){return(
htl.html`     <pre>     <h1>  Stochastic Oscillator </pre>`
)}

function _include7(Inputs){return(
Inputs.toggle({label: "Stochastic Oscillator"})
)}

function _y3(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([d3.min(data, d => +d.stochastic_oscillator_sma), d3.max(data, d => +d.stochastic_oscillator_sma)])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis3(margin,d3,y3,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y3).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _chart3(d3,width,height,x,y3,include7,data,so_ul,so_ll,xAxis,yAxis3)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x.copy(); // x, but with a new domain.
  const zy = y3.copy(); // x, but with a new domain.

  var line7 = d3.line()
  var path7 = svg.append("path")
  if (include7 == 1) {
    line7 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.stochastic_oscillator_sma));

    path7 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line7(data));
  }

  var line72 = d3.line()
  var path72 = svg.append("path")
  if (include7 == 1) {
    line72 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(so_ul));

    path72 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line72(data));
  }

  var line73 = d3.line()
  var path73 = svg.append("path")
  if (include7 == 1) {
    line73 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(so_ll));

    path73 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line73(data));
  }
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis3, zy);

  if (include7){
    return Object.assign(svg.node(), {
      update(domain) {
        const t = svg.transition().duration(750);
        zx.domain(domain);
        gx.transition(t).call(xAxis, zx);
        // ADD PATH TRANSITIONS HERE SO THAT THEY SCALE WITH VIEWING WINDOW
        path7.transition(t).attr("d", line7(data));
      }
    });
  }
}


function _44(htl){return(
htl.html`     <pre>     <h1>  Price to SMA Ratio </pre>`
)}

function _include8(Inputs){return(
Inputs.toggle({label: "Price to SMA Ratio"})
)}

function _y4(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([d3.min(data, d => +d.price_to_SMA_ratio), d3.max(data, d => +d.price_to_SMA_ratio)])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis4(margin,d3,y4,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y4).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _chart4(d3,width,height,x,y4,include8,data,smathreshold,xAxis,yAxis4)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x.copy(); // x, but with a new domain.
  const zy = y4.copy(); // x, but with a new domain.

 var line8 = d3.line()
  var path8 = svg.append("path")
  if (include8 == 1) {
    line8 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.price_to_SMA_ratio));

    path8 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line8(data));
  }

  var line81 = d3.line()
  var path81 = svg.append("path")
  if (include8 == 1) {
    line81 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(smathreshold));

    path81 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line81(data));
  }

  var line82 = d3.line()
  var path82 = svg.append("path")
  if (include8 == 1) {
    line82 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(-1*smathreshold));

    path82 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line82(data));
  }
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis4, zy);

  if (include8){
    return Object.assign(svg.node(), {
      update(domain) {
        const t = svg.transition().duration(750);
        zx.domain(domain);
        gx.transition(t).call(xAxis, zx);
        // ADD PATH TRANSITIONS HERE SO THAT THEY SCALE WITH VIEWING WINDOW
        path8.transition(t).attr("d", line8(data));
      }
    });
  }
}


function _49(htl){return(
htl.html`     <pre>     <h1>  Momentum </pre>`
)}

function _include9(Inputs){return(
Inputs.toggle({label: "Momentum"})
)}

function _data2(data){return(
data.map(d => d.momentum)
)}

function _y5(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([d3.min(data, d => +d.momentum), d3.max(data, d => +d.momentum)])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis5(margin,d3,y5,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y5).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _chart5(d3,width,height,x,y5,include9,data,momentumth,xAxis,yAxis5)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x.copy(); // x, but with a new domain.
  const zy = y5.copy(); // x, but with a new domain.

  var line9 = d3.line()
  var path9 = svg.append("path")
  if (include9 == 1) {
    line9 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(d.momentum));

    path9 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line9(data));
  }

  var line91 = d3.line()
  var path91 = svg.append("path")
  if (include9 == 1) {
    line91 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(momentumth));

    path91 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line91(data));
  }

  var line92 = d3.line()
  var path92 = svg.append("path")
  if (include9 == 1) {
    line92 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(-1*momentumth));

    path92 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line92(data));
  }
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis5, zy);

  if (include9){
    return Object.assign(svg.node(), {
      update(domain) {
        const t = svg.transition().duration(750);
        zx.domain(domain);
        gx.transition(t).call(xAxis, zx);
        // ADD PATH TRANSITIONS HERE SO THAT THEY SCALE WITH VIEWING WINDOW
        path9.transition(t).attr("d", line9(data));
      }
    });
  }
}


function _55(htl){return(
htl.html`     <pre>     <h1>  Sentiment </pre>`
)}

function _include10(Inputs){return(
Inputs.toggle({label: "Sentiment"})
)}

function _y6(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([d3.min(data, d => +d.avg_compound_sentiment), d3.max(data, d => +d.avg_compound_sentiment)])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis6(margin,d3,y6,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y6).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _chart6(d3,width,height,x,y6,include10,data,sentimentth,xAxis,yAxis6)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x.copy(); // x, but with a new domain.
  const zy = y6.copy(); // x, but with a new domain.

 var line10 = d3.line()
  var path10 = svg.append("path")
  if (include10 == 1) {
    line10 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.avg_compound_sentiment));

    path10 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line10(data));
  }

  var line102 = d3.line()
  var path102 = svg.append("path")
  if (include10 == 1) {
    line102 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(-1*sentimentth));

    path102 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line102(data));
  }

  var line103 = d3.line()
  var path103 = svg.append("path")
  if (include10 == 1) {
    line103 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(sentimentth));

    path103 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line103(data));
  }

  
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis6, zy);

  if (include10){
    return Object.assign(svg.node(), {
      update(domain) {
        const t = svg.transition().duration(750);
        zx.domain(domain);
        gx.transition(t).call(xAxis, zx);
        // ADD PATH TRANSITIONS HERE SO THAT THEY SCALE WITH VIEWING WINDOW
        path10.transition(t).attr("d", line10(data));
      }
    });
  }
}


function _60(htl){return(
htl.html`     <pre>     <h1>  MACD </pre>`
)}

function _include11(Inputs){return(
Inputs.toggle({label: "MACD", value: false})
)}

function _macd_inputs(Inputs){return(
Inputs.checkbox(["MACD", "MACD Signal", "MACD Raw"], {label: "Select Features:"})
)}

function _y7(d3,min_macd,max_macd,height,margin){return(
d3.scaleLinear()
    .domain([min_macd,max_macd])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis7(margin,d3,y7,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y7).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _max_macd(d3,data){return(
d3.max([d3.max(data, function(d) { return +d.MACD; }), d3.max(data, function(d) { return +d.MACD_signal; }), d3.max(data, function(d) { return +d.MACD_raw; })])
)}

function _min_macd(d3,data){return(
d3.min([d3.min(data, function(d) { return +d.MACD; }), d3.min(data, function(d) { return +d.MACD_signal; }), d3.min(data, function(d) { return +d.MACD_raw; })])
)}

function _chart7(d3,width,height,x,y7,include11,data,macd_inputs,xAxis,yAxis7)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x.copy(); // x, but with a new domain.
  const zy = y7.copy(); // x, but with a new domain.

  var line11 = d3.line()
  var path11 = svg.append("path")
  if (include11 == 1) {
    line11 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.MACD));

    path11 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line11(data));
  }

  var line112 = d3.line()
  var path112 = svg.append("path")
  if (macd_inputs.includes("MACD Signal")) {
    line112 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.MACD_raw));

    path112 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line112(data));
  }

  var line113 = d3.line()
  var path113 = svg.append("path")
  if (macd_inputs.includes("MACD Raw")) {
    line113 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.MACD_signal));

    path113 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line113(data));
  }
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis7, zy);

  if (include11){
    return Object.assign(svg.node(), {
      update(domain) {
        const t = svg.transition().duration(750);
        zx.domain(domain);
        gx.transition(t).call(xAxis, zx);
        // ADD PATH TRANSITIONS HERE SO THAT THEY SCALE WITH VIEWING WINDOW
        path11.transition(t).attr("d", line11(data));
        path112.transition(t).attr("d", line112(data));
        path113.transition(t).attr("d", line113(data));
      }
    });
  }
}


function _68(htl){return(
htl.html`     <pre>     <h1>  Training Data </pre>`
)}

function _include12(Inputs){return(
Inputs.toggle({label: "Training QL"})
)}

function _include13(Inputs){return(
Inputs.toggle({label: "Training Benchmark"})
)}

function _datasettraining(data){return(
data.filter(d => d.test_or_train == 'train')
)}

function _max_y(d3,datasettraining){return(
d3.max([d3.max(datasettraining, function(d) { return +d.QL; }), d3.max(datasettraining, function(d) { return +d.benchmark; })])
)}

function _min_y(d3,datasettraining){return(
d3.min([d3.min(datasettraining, function(d) { return +d.QL; }), d3.min(datasettraining, function(d) { return +d.benchmark; })])
)}

function _y8(d3,min_y,max_y,height,margin){return(
d3.scaleLinear()
    // .domain(d3.min([d3.min(datasettraining.QL),d3.min(datasettraining.QL)]),d3.max([d3.max(datasettraining.QL),d3.max(datasettraining.QL)]))
    .domain([min_y,max_y])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis8(margin,d3,y8,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y8).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _x8(d3,datasettraining,margin,width){return(
d3.scaleUtc()
    .domain(d3.extent(datasettraining, d => d.TradeDate))
    .range([margin.left, width - margin.right])
)}

function _77(d3,datasettraining){return(
d3.extent(datasettraining, d => d.TradeDate)
)}

function _xAxis8(height,margin,d3,x8,width){return(
g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x8).ticks(width / 80).tickSizeOuter(0))
)}

function _orderstraining(data){return(
data.filter(d => ((d.test_or_train == 'train') & (d.orders == 'BUY' | d.orders == 'BUY')))
)}

function _orderstraining2(orderstraining){return(
orderstraining.map(d => [d.TradeDate, d.orders])
)}

function _chart8(d3,width,height,x8,y8,include12,datasettraining,include13,xAxis8,yAxis8)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-20,-10, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x8.copy(); // x, but with a new domain.
  const zy = y8.copy(); // x, but with a new domain.

 var line8 = d3.line()
  var path8 = svg.append("path")
  if (include12 == 1) {
    line8 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.QL));

    path8 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line8(datasettraining));
  }

  var line82 = d3.line()
  var path82 = svg.append("path")
  if (include13 == 1) {
    line82 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.benchmark+ 500000));

    path82 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "orange")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line82(datasettraining));
  }

  for (let index = 0; index < datasettraining.length; ++index) {

    if (datasettraining[index].orders == 'BUY'){
        svg.append("circle")
  	        	.attr("class","circle")
  		        .attr("cx",zx(datasettraining[index].TradeDate))
  		        .attr("cy",zy(datasettraining[index].benchmark + 500000))
  		        .attr("r",5)
  		        .style("stroke","#00ff00")
  		        .style("fill","#00ff00")
    } else if (datasettraining[index].orders == 'SELL'){
      svg.append("circle")
  	        	.attr("class","circle")
  		        .attr("cx",zx(datasettraining[index].TradeDate))
  		        .attr("cy",zy(datasettraining[index].benchmark + 500000))
  		        .attr("r",5)
  		        .style("stroke","#ff0000")
  		        .style("fill","#ff0000")
    }
  }
  
  const gx = svg.append("g")
      .call(xAxis8, zx);

  const gy = svg.append("g")
      .call(yAxis8, zy);

  if (include12 | include13){
    return Object.assign(svg.node(), {
      update(domain) {
        const t = svg.transition().duration(750);
        zx.domain(domain);
        gx.transition(t).call(xAxis8, zx);
        // ADD PATH TRANSITIONS HERE SO THAT THEY SCALE WITH VIEWING WINDOW
      }
    });
  }
}


function _82(htl){return(
htl.html`     <pre>     <h1>  Testing Data </pre>`
)}

function _include14(Inputs){return(
Inputs.toggle({label: "Testing QL"})
)}

function _include15(Inputs){return(
Inputs.toggle({label: "Testing Benchmark"})
)}

function _datasetesting(data){return(
data.filter(d => d.test_or_train == 'test')
)}

function _max_y2(d3,datasetesting){return(
d3.max([d3.max(datasetesting, function(d) { return +d.QL; }), d3.max(datasetesting, function(d) { return +d.benchmark; })])
)}

function _min_y2(d3,datasetesting){return(
d3.min([d3.min(datasetesting, function(d) { return +d.QL; }), d3.min(datasetesting, function(d) { return +d.benchmark; })])
)}

function _y9(d3,min_y2,max_y2,height,margin){return(
d3.scaleLinear()
    .domain([min_y2 ,max_y2])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis9(margin,d3,y9,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y9).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _x9(d3,datasetesting,margin,width){return(
d3.scaleUtc()
    .domain(d3.extent(datasetesting, d => d.TradeDate))
    .range([margin.left, width - margin.right])
)}

function _91(d3,datasetesting){return(
d3.extent(datasetesting, d => d.TradeDate)
)}

function _xAxis9(height,margin,d3,x9,width){return(
g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x9).ticks(width / 80).tickSizeOuter(0))
)}

function _chart9(d3,width,height,x9,y9,include14,datasetesting,include15,xAxis9,yAxis9)
{
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-20, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  const zx = x9.copy(); // x, but with a new domain.
  const zy = y9.copy(); // x, but with a new domain.

 var line9 = d3.line()
  var path9 = svg.append("path")
  if (include14 == 1) {
    line9 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.QL));

    path9 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line9(datasetesting));
  }

  var line10 = d3.line()
  var path10 = svg.append("path")
  if (include15 == 1) {
    line10 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.benchmark + 500000));

    path10 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "orange")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line10(datasetesting));
  }

  for (let index = 0; index < datasetesting.length; ++index) {

    if (datasetesting[index].orders == 'BUY'){
        svg.append("circle")
  	        	.attr("class","circle")
  		        .attr("cx",zx(datasetesting[index].TradeDate))
  		        .attr("cy",zy(datasetesting[index].benchmark+ 500000))
  		        .attr("r",5)
  		        .style("stroke","#00ff00")
  		        .style("fill","#00ff00")

    } else if (datasetesting[index].orders == 'SELL'){
      svg.append("circle")
  	        	.attr("class","circle")
  		        .attr("cx",zx(datasetesting[index].TradeDate))
  		        .attr("cy",zy(datasetesting[index].benchmark+ 500000))
  		        .attr("r",5)
  		        .style("stroke","#ff0000")
  		        .style("fill","#ff0000")
    }
  }
  
  const gx = svg.append("g")
      .call(xAxis9, zx);

  const gy = svg.append("g")
      .call(yAxis9, zy);

  if (include14 | include15){
    return Object.assign(svg.node(), {
      update(domain) {
        const t = svg.transition().duration(750);
        zx.domain(domain);
        gx.transition(t).call(xAxis9, zx);
        // ADD PATH TRANSITIONS HERE SO THAT THEY SCALE WITH VIEWING WINDOW
      }
    });
  }
}


function _update(chart,timeframe){return(
chart.update(timeframe)
)}

function _update2(chart2,timeframe){return(
chart2.update(timeframe)
)}

function _update3(chart3,timeframe){return(
chart3.update(timeframe)
)}

function _update4(chart4,timeframe){return(
chart4.update(timeframe)
)}

function _update5(chart5,timeframe){return(
chart5.update(timeframe)
)}

function _update6(chart6,timeframe){return(
chart6.update(timeframe)
)}

function _update7(chart7,timeframe){return(
chart7.update(timeframe)
)}

function _update8(chart8,timeframe){return(
chart8.update(timeframe)
)}

function _update9(chart9,timeframe){return(
chart9.update(timeframe)
)}

function _103(md){return(
md`---

## Appendix`
)}

function _timeframe(dateone,datetwo){return(
[dateone,datetwo]
)}

function _datep(d3){return(
d3.timeFormat("%Y-%m-%d")
)}

function _params(datep,training_startdate,training_enddate,testing_startdate,testing_enddate,smawindow,bbwindow,bbstdev,so_window,so_window_sma,obv,macd,include_sentiment,mom_window,alpha,gamma,rar,radr,smathreshold,so_ul,so_ll,momentumth,sentimentth){return(
{
"ticker": "BTC",
"training_sd": datep(training_startdate),
"training_ed": datep(training_enddate),
"test_sd": datep(testing_startdate),
"test_ed": datep(testing_enddate),
"sv": 500000,
"sma_window": smawindow,
"bollinger_window": bbwindow,
"bollinger_stdvs": bbstdev,
"so_window": so_window,
"so_window_sma": so_window_sma,
"obv": obv,
"macd": macd,
"include_sentiment": include_sentiment,
"mom_window": mom_window,
"alpha": alpha,
"gamma": gamma,
"rar": rar,
"radr": radr,
"sma_threshold": smathreshold,
"so_ul": so_ul,
"so_ll": so_ll,
"mom_threshold": momentumth,
"sentiment_threshold": sentimentth
}
)}

function _queryString(params){return(
Object.keys(params).map(function(key) {
return key + '=' + params[key]
}).join('&')
)}

function _url(queryString){return(
"http://127.0.0.1:5001/run_qlearner?" + queryString
)}

function _url2(queryString){return(
"http://127.0.0.1:5001/run_gridsearch?" + queryString
)}

function _dataset2(rf,qlgs,url,url2)
{
  if (rf){
    if (qlgs == "Run QLearner"){
      return fetch(url).then(response => response.json()).then(function(data) {return data})
    } else if (qlgs == "Run GridSearch")
      return fetch(url2).then(response => response.json()).then(function(data) {return data})
  }
}


function _111(dataset2){return(
dataset2
)}

function _cleanedData(dataset2){return(
dataset2.map(d => ({
  'bollinger_sma': parseFloat(d.bollinger_sma),
  'bollinger_band_upper': parseFloat(d.bollinger_band_upper),
  'bollinger_band_lower': parseFloat(d.bollinger_band_lower),
  'TradeDate': new Date(d.TradeDate),
  'rolling_avg': parseFloat(d.rolling_avg),
  'Adj_Close': parseFloat(d.Adj_Close),
  'bollinger_band_percentage': parseFloat(d.bollinger_band_percentage),
  'stochastic_oscillator_sma': parseFloat(d.stochastic_oscillator_sma),
  'price_to_SMA_ratio': parseFloat(d.price_to_SMA_ratio),
  'momentum': parseFloat(d.momentum),
  'avg_compound_sentiment': parseFloat(d.avg_compound_sentiment),
  'MACD_raw': parseFloat(d.MACD_raw),
  'MACD_signal': parseFloat(d.MACD_signal),
  'MACD': parseFloat(d.MACD),
  'price_to_SMA_ratio': parseFloat(d.price_to_SMA_ratio),
  'avg_compound_sentiment': parseFloat(d.avg_compound_sentiment),
  'MACD_raw': parseFloat(d.MACD_raw),
  'MACD_signal': parseFloat(d.MACD_signal),
  'MACD': parseFloat(d.MACD),
  "QL": parseFloat(d.QL),
  "benchmark": parseFloat(d.benchmark),
  "test_or_train": d.test_or_train,
  "orders": d.orders
}))
)}

function _data(cleanedData){return(
cleanedData
)}

function _114(data){return(
console.log(data)
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

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("viewof include_sentiment")).define("viewof include_sentiment", ["Inputs"], _include_sentiment);
  main.variable(observer("include_sentiment")).define("include_sentiment", ["Generators", "viewof include_sentiment"], (G, _) => G.input(_));
  main.variable(observer("viewof macd")).define("viewof macd", ["Inputs"], _macd);
  main.variable(observer("macd")).define("macd", ["Generators", "viewof macd"], (G, _) => G.input(_));
  main.variable(observer("viewof obv")).define("viewof obv", ["Inputs"], _obv);
  main.variable(observer("obv")).define("obv", ["Generators", "viewof obv"], (G, _) => G.input(_));
  main.variable(observer("viewof alpha")).define("viewof alpha", ["Inputs"], _alpha);
  main.variable(observer("alpha")).define("alpha", ["Generators", "viewof alpha"], (G, _) => G.input(_));
  main.variable(observer("viewof gamma")).define("viewof gamma", ["Inputs"], _gamma);
  main.variable(observer("gamma")).define("gamma", ["Generators", "viewof gamma"], (G, _) => G.input(_));
  main.variable(observer("viewof rar")).define("viewof rar", ["Inputs"], _rar);
  main.variable(observer("rar")).define("rar", ["Generators", "viewof rar"], (G, _) => G.input(_));
  main.variable(observer("viewof radr")).define("viewof radr", ["Inputs"], _radr);
  main.variable(observer("radr")).define("radr", ["Generators", "viewof radr"], (G, _) => G.input(_));
  main.variable(observer("viewof smathreshold")).define("viewof smathreshold", ["Inputs"], _smathreshold);
  main.variable(observer("smathreshold")).define("smathreshold", ["Generators", "viewof smathreshold"], (G, _) => G.input(_));
  main.variable(observer("viewof momentumth")).define("viewof momentumth", ["Inputs"], _momentumth);
  main.variable(observer("momentumth")).define("momentumth", ["Generators", "viewof momentumth"], (G, _) => G.input(_));
  main.variable(observer("viewof sentimentth")).define("viewof sentimentth", ["Inputs"], _sentimentth);
  main.variable(observer("sentimentth")).define("sentimentth", ["Generators", "viewof sentimentth"], (G, _) => G.input(_));
  main.variable(observer("viewof so_ul")).define("viewof so_ul", ["Inputs"], _so_ul);
  main.variable(observer("so_ul")).define("so_ul", ["Generators", "viewof so_ul"], (G, _) => G.input(_));
  main.variable(observer("viewof so_ll")).define("viewof so_ll", ["Inputs"], _so_ll);
  main.variable(observer("so_ll")).define("so_ll", ["Generators", "viewof so_ll"], (G, _) => G.input(_));
  main.variable(observer("viewof training_startdate")).define("viewof training_startdate", ["Inputs"], _training_startdate);
  main.variable(observer("training_startdate")).define("training_startdate", ["Generators", "viewof training_startdate"], (G, _) => G.input(_));
  main.variable(observer("viewof training_enddate")).define("viewof training_enddate", ["Inputs"], _training_enddate);
  main.variable(observer("training_enddate")).define("training_enddate", ["Generators", "viewof training_enddate"], (G, _) => G.input(_));
  main.variable(observer("viewof testing_startdate")).define("viewof testing_startdate", ["Inputs"], _testing_startdate);
  main.variable(observer("testing_startdate")).define("testing_startdate", ["Generators", "viewof testing_startdate"], (G, _) => G.input(_));
  main.variable(observer("viewof testing_enddate")).define("viewof testing_enddate", ["Inputs"], _testing_enddate);
  main.variable(observer("testing_enddate")).define("testing_enddate", ["Generators", "viewof testing_enddate"], (G, _) => G.input(_));
  main.variable(observer("viewof smawindow")).define("viewof smawindow", ["Inputs"], _smawindow);
  main.variable(observer("smawindow")).define("smawindow", ["Generators", "viewof smawindow"], (G, _) => G.input(_));
  main.variable(observer("viewof bbwindow")).define("viewof bbwindow", ["Inputs"], _bbwindow);
  main.variable(observer("bbwindow")).define("bbwindow", ["Generators", "viewof bbwindow"], (G, _) => G.input(_));
  main.variable(observer("viewof bbstdev")).define("viewof bbstdev", ["Inputs"], _bbstdev);
  main.variable(observer("bbstdev")).define("bbstdev", ["Generators", "viewof bbstdev"], (G, _) => G.input(_));
  main.variable(observer("viewof so_window")).define("viewof so_window", ["Inputs"], _so_window);
  main.variable(observer("so_window")).define("so_window", ["Generators", "viewof so_window"], (G, _) => G.input(_));
  main.variable(observer("viewof so_window_sma")).define("viewof so_window_sma", ["Inputs"], _so_window_sma);
  main.variable(observer("so_window_sma")).define("so_window_sma", ["Generators", "viewof so_window_sma"], (G, _) => G.input(_));
  main.variable(observer("viewof mom_window")).define("viewof mom_window", ["Inputs"], _mom_window);
  main.variable(observer("mom_window")).define("mom_window", ["Generators", "viewof mom_window"], (G, _) => G.input(_));
  main.variable(observer()).define(["htl"], _24);
  main.variable(observer("viewof qlgs")).define("viewof qlgs", ["Inputs"], _qlgs);
  main.variable(observer("qlgs")).define("qlgs", ["Generators", "viewof qlgs"], (G, _) => G.input(_));
  main.variable(observer("viewof rf")).define("viewof rf", ["Inputs"], _rf);
  main.variable(observer("rf")).define("rf", ["Generators", "viewof rf"], (G, _) => G.input(_));
  main.variable(observer()).define(["htl"], _27);
  main.variable(observer("viewof dateone")).define("viewof dateone", ["Inputs","training_startdate"], _dateone);
  main.variable(observer("dateone")).define("dateone", ["Generators", "viewof dateone"], (G, _) => G.input(_));
  main.variable(observer("viewof datetwo")).define("viewof datetwo", ["Inputs","testing_enddate"], _datetwo);
  main.variable(observer("datetwo")).define("datetwo", ["Generators", "viewof datetwo"], (G, _) => G.input(_));
  main.variable(observer()).define(["htl"], _30);
  main.variable(observer("viewof inchart1")).define("viewof inchart1", ["Inputs"], _inchart1);
  main.variable(observer("inchart1")).define("inchart1", ["Generators", "viewof inchart1"], (G, _) => G.input(_));
  main.variable(observer("viewof bbg_inputs")).define("viewof bbg_inputs", ["Inputs"], _bbg_inputs);
  main.variable(observer("bbg_inputs")).define("bbg_inputs", ["Generators", "viewof bbg_inputs"], (G, _) => G.input(_));
  main.variable(observer("chart")).define("chart", ["d3","width","height","x","y","bbg_inputs","data","xAxis","yAxis","inchart1"], _chart);
  main.variable(observer()).define(["htl"], _34);
  main.variable(observer("viewof include6")).define("viewof include6", ["Inputs"], _include6);
  main.variable(observer("include6")).define("include6", ["Generators", "viewof include6"], (G, _) => G.input(_));
  main.variable(observer("y2")).define("y2", ["d3","data","height","margin"], _y2);
  main.variable(observer("yAxis2")).define("yAxis2", ["margin","d3","y2","height"], _yAxis2);
  main.variable(observer("chart2")).define("chart2", ["d3","width","height","x","y2","include6","data","xAxis","yAxis2"], _chart2);
  main.variable(observer()).define(["htl"], _39);
  main.variable(observer("viewof include7")).define("viewof include7", ["Inputs"], _include7);
  main.variable(observer("include7")).define("include7", ["Generators", "viewof include7"], (G, _) => G.input(_));
  main.variable(observer("y3")).define("y3", ["d3","data","height","margin"], _y3);
  main.variable(observer("yAxis3")).define("yAxis3", ["margin","d3","y3","height"], _yAxis3);
  main.variable(observer("chart3")).define("chart3", ["d3","width","height","x","y3","include7","data","so_ul","so_ll","xAxis","yAxis3"], _chart3);
  main.variable(observer()).define(["htl"], _44);
  main.variable(observer("viewof include8")).define("viewof include8", ["Inputs"], _include8);
  main.variable(observer("include8")).define("include8", ["Generators", "viewof include8"], (G, _) => G.input(_));
  main.variable(observer("y4")).define("y4", ["d3","data","height","margin"], _y4);
  main.variable(observer("yAxis4")).define("yAxis4", ["margin","d3","y4","height"], _yAxis4);
  main.variable(observer("chart4")).define("chart4", ["d3","width","height","x","y4","include8","data","smathreshold","xAxis","yAxis4"], _chart4);
  main.variable(observer()).define(["htl"], _49);
  main.variable(observer("viewof include9")).define("viewof include9", ["Inputs"], _include9);
  main.variable(observer("include9")).define("include9", ["Generators", "viewof include9"], (G, _) => G.input(_));
  main.variable(observer("data2")).define("data2", ["data"], _data2);
  main.variable(observer("y5")).define("y5", ["d3","data","height","margin"], _y5);
  main.variable(observer("yAxis5")).define("yAxis5", ["margin","d3","y5","height"], _yAxis5);
  main.variable(observer("chart5")).define("chart5", ["d3","width","height","x","y5","include9","data","momentumth","xAxis","yAxis5"], _chart5);
  main.variable(observer()).define(["htl"], _55);
  main.variable(observer("viewof include10")).define("viewof include10", ["Inputs"], _include10);
  main.variable(observer("include10")).define("include10", ["Generators", "viewof include10"], (G, _) => G.input(_));
  main.variable(observer("y6")).define("y6", ["d3","data","height","margin"], _y6);
  main.variable(observer("yAxis6")).define("yAxis6", ["margin","d3","y6","height"], _yAxis6);
  main.variable(observer("chart6")).define("chart6", ["d3","width","height","x","y6","include10","data","sentimentth","xAxis","yAxis6"], _chart6);
  main.variable(observer()).define(["htl"], _60);
  main.variable(observer("viewof include11")).define("viewof include11", ["Inputs"], _include11);
  main.variable(observer("include11")).define("include11", ["Generators", "viewof include11"], (G, _) => G.input(_));
  main.variable(observer("viewof macd_inputs")).define("viewof macd_inputs", ["Inputs"], _macd_inputs);
  main.variable(observer("macd_inputs")).define("macd_inputs", ["Generators", "viewof macd_inputs"], (G, _) => G.input(_));
  main.variable(observer("y7")).define("y7", ["d3","min_macd","max_macd","height","margin"], _y7);
  main.variable(observer("yAxis7")).define("yAxis7", ["margin","d3","y7","height"], _yAxis7);
  main.variable(observer("max_macd")).define("max_macd", ["d3","data"], _max_macd);
  main.variable(observer("min_macd")).define("min_macd", ["d3","data"], _min_macd);
  main.variable(observer("chart7")).define("chart7", ["d3","width","height","x","y7","include11","data","macd_inputs","xAxis","yAxis7"], _chart7);
  main.variable(observer()).define(["htl"], _68);
  main.variable(observer("viewof include12")).define("viewof include12", ["Inputs"], _include12);
  main.variable(observer("include12")).define("include12", ["Generators", "viewof include12"], (G, _) => G.input(_));
  main.variable(observer("viewof include13")).define("viewof include13", ["Inputs"], _include13);
  main.variable(observer("include13")).define("include13", ["Generators", "viewof include13"], (G, _) => G.input(_));
  main.variable(observer("datasettraining")).define("datasettraining", ["data"], _datasettraining);
  main.variable(observer("max_y")).define("max_y", ["d3","datasettraining"], _max_y);
  main.variable(observer("min_y")).define("min_y", ["d3","datasettraining"], _min_y);
  main.variable(observer("y8")).define("y8", ["d3","min_y","max_y","height","margin"], _y8);
  main.variable(observer("yAxis8")).define("yAxis8", ["margin","d3","y8","height"], _yAxis8);
  main.variable(observer("x8")).define("x8", ["d3","datasettraining","margin","width"], _x8);
  main.variable(observer()).define(["d3","datasettraining"], _77);
  main.variable(observer("xAxis8")).define("xAxis8", ["height","margin","d3","x8","width"], _xAxis8);
  main.variable(observer("orderstraining")).define("orderstraining", ["data"], _orderstraining);
  main.variable(observer("orderstraining2")).define("orderstraining2", ["orderstraining"], _orderstraining2);
  main.variable(observer("chart8")).define("chart8", ["d3","width","height","x8","y8","include12","datasettraining","include13","xAxis8","yAxis8"], _chart8);
  main.variable(observer()).define(["htl"], _82);
  main.variable(observer("viewof include14")).define("viewof include14", ["Inputs"], _include14);
  main.variable(observer("include14")).define("include14", ["Generators", "viewof include14"], (G, _) => G.input(_));
  main.variable(observer("viewof include15")).define("viewof include15", ["Inputs"], _include15);
  main.variable(observer("include15")).define("include15", ["Generators", "viewof include15"], (G, _) => G.input(_));
  main.variable(observer("datasetesting")).define("datasetesting", ["data"], _datasetesting);
  main.variable(observer("max_y2")).define("max_y2", ["d3","datasetesting"], _max_y2);
  main.variable(observer("min_y2")).define("min_y2", ["d3","datasetesting"], _min_y2);
  main.variable(observer("y9")).define("y9", ["d3","min_y2","max_y2","height","margin"], _y9);
  main.variable(observer("yAxis9")).define("yAxis9", ["margin","d3","y9","height"], _yAxis9);
  main.variable(observer("x9")).define("x9", ["d3","datasetesting","margin","width"], _x9);
  main.variable(observer()).define(["d3","datasetesting"], _91);
  main.variable(observer("xAxis9")).define("xAxis9", ["height","margin","d3","x9","width"], _xAxis9);
  main.variable(observer("chart9")).define("chart9", ["d3","width","height","x9","y9","include14","datasetesting","include15","xAxis9","yAxis9"], _chart9);
  main.variable(observer("update")).define("update", ["chart","timeframe"], _update);
  main.variable(observer("update2")).define("update2", ["chart2","timeframe"], _update2);
  main.variable(observer("update3")).define("update3", ["chart3","timeframe"], _update3);
  main.variable(observer("update4")).define("update4", ["chart4","timeframe"], _update4);
  main.variable(observer("update5")).define("update5", ["chart5","timeframe"], _update5);
  main.variable(observer("update6")).define("update6", ["chart6","timeframe"], _update6);
  main.variable(observer("update7")).define("update7", ["chart7","timeframe"], _update7);
  main.variable(observer("update8")).define("update8", ["chart8","timeframe"], _update8);
  main.variable(observer("update9")).define("update9", ["chart9","timeframe"], _update9);
  main.variable(observer()).define(["md"], _103);
  main.variable(observer("timeframe")).define("timeframe", ["dateone","datetwo"], _timeframe);
  main.variable(observer("datep")).define("datep", ["d3"], _datep);
  main.variable(observer("params")).define("params", ["datep","training_startdate","training_enddate","testing_startdate","testing_enddate","smawindow","bbwindow","bbstdev","so_window","so_window_sma","obv","macd","include_sentiment","mom_window","alpha","gamma","rar","radr","smathreshold","so_ul","so_ll","momentumth","sentimentth"], _params);
  main.variable(observer("queryString")).define("queryString", ["params"], _queryString);
  main.variable(observer("url")).define("url", ["queryString"], _url);
  main.variable(observer("url2")).define("url2", ["queryString"], _url2);
  main.variable(observer("dataset2")).define("dataset2", ["rf","qlgs","url","url2"], _dataset2);
  main.variable(observer()).define(["dataset2"], _111);
  main.variable(observer("cleanedData")).define("cleanedData", ["dataset2"], _cleanedData);
  main.variable(observer("data")).define("data", ["cleanedData"], _data);
  main.variable(observer()).define(["data"], _114);
  main.variable(observer("xAxis")).define("xAxis", ["x","height","margin","d3","width"], _xAxis);
  main.variable(observer("yAxis")).define("yAxis", ["margin","d3","y","height"], _yAxis);
  main.variable(observer("height")).define("height", _height);
  main.variable(observer("margin")).define("margin", _margin);
  main.variable(observer("x")).define("x", ["d3","data","margin","width"], _x);
  main.variable(observer("y")).define("y", ["d3","data","height","margin"], _y);
  return main;
}
