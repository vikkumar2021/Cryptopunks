import define1 from "./7a9e12f9fb3d8e06@459.js";

function _1(md){return(
md`# CryptoPunks&#8482; BTC + Sentiment Learner
`
)}

function _2(htl){return(
htl.html`<p>Howdy Yellow Jackets, </p>
  
<p>Welcome to the CryptoPunks&#8482; Money Machine!</p>

<p>Get ready to use machine learning to beat the market. This website currently supports Bitcoin (BTC) data only :) </p>

<p>The two algorithms available are: Q-Learning and GridSearch. Select your indicators and fetch the data to get started!!! </p>

<p>  </p>

<p><b>Tips:</b>
  <ul>
  <li>Sentiment, MACD and On Balance Volume are not included by default. Check the box for inclusion.</li>
    <p>  </p>
  <li>Training time range must be before testing time range and they must not overlap.</li>
    <p>  </p>
  <li>Open up the individual graphs wanted for display by checking the boxes.</li>
</ul>

</p>`
)}

function _3(htl){return(
htl.html`<p>  </p>`
)}

function _4(md){return(
md`### Pick your indicators:`
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

function _27(htl){return(
htl.html`<p>  </p>`
)}

function _28(htl){return(
htl.html`     <pre>     <h1>  Run the Q Learner or Grid Search Here </pre>`
)}

function _qlgs(Inputs){return(
Inputs.select(["Run QLearner", "Run GridSearch"], {label: "QLearner or Grid Search:"})
)}

function _rf(Inputs){return(
Inputs.toggle({label: "Fetch Data", value: false})
)}

function _31(htl){return(
htl.html`<p>  </p>`
)}

function _32(htl){return(
htl.html`     <pre>     <h1>  Select viewing window </pre>`
)}

function _dateone(Inputs,training_startdate){return(
Inputs.date({value: training_startdate, label: "StartDate"})
)}

function _datetwo(Inputs,testing_enddate){return(
Inputs.date({value: testing_enddate, label: "EndDate"})
)}

function _35(htl){return(
htl.html`<p>  </p>`
)}

function _36(htl){return(
htl.html`     <pre>     <h1> Q-Learner / GridSearch </pre>`
)}

function _37(htl){return(
htl.html`     <pre>     <h2>  Training Data Graph </pre>`
)}

function _training_inputs(Inputs){return(
Inputs.checkbox(["Training QL", "Training Benchmark"], {label: "Select Features:"})
)}

function _chart8(d3,width,height,x8,y8,training_inputs,datasettraining,include_sentiment,xAxis8,yAxis8)
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
  if (training_inputs.includes("Training QL")) {
    line8 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.QL));

    path8 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line8(datasettraining));
    const leg1_shape = svg.append("circle").attr("cx",100).attr("cy",20).attr("r", 6).style("fill", "blue")
    const leg1_text = svg.append("text").attr("x", 110).attr("y", 20).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Q Learner").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line82 = d3.line()
  var path82 = svg.append("path")
  if (training_inputs.includes("Training Benchmark")) {
    line82 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.benchmark+ 500000));

    path82 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "orange")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line82(datasettraining));
    const leg1_shape = svg.append("circle").attr("cx",100).attr("cy",40).attr("r", 6).style("fill", "orange")
    const leg1_text = svg.append("text").attr("x", 110).attr("y", 40).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Benchmark").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  if (training_inputs.includes("Training Benchmark")) {
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
  const leg3_shape = svg.append("circle").attr("cx",100).attr("cy",60).attr("r", 6).style("fill", "#00ff00")
  const leg3_text = svg.append("text").attr("x", 110).attr("y", 60).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Buy").style("font-size", "13px").attr("alignment-baseline","middle")
  
  const leg4_shape = svg.append("circle").attr("cx",100).attr("cy",80).attr("r", 6).style("fill", "#ff0000")
  const leg4_text = svg.append("text").attr("x", 110).attr("y", 80).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Sell").style("font-size", "13px").attr("alignment-baseline","middle")
  }

   //DYNAMIC TITLE (W or W/O SENTIMENT ANALYSIS
  if (include_sentiment) {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Training Data Graph Using Sentiment Data");
  }
  else {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Training Data Graph Without Using Sentiment Data");
  }
 
  
  const gx = svg.append("g")
      .call(xAxis8, zx);

  const gy = svg.append("g")
      .call(yAxis8, zy);

  //  AXIS LABEL
  const y_axis_label = svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y",0 )
      .attr("x",-180)
      .attr("transform", "rotate(-90)")
      .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
      .style("font-size", "12px")
      .text("Portfolio Value USD");
  
    //AXIS LABEL
  const x_axis_label = svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width - 550)
    .attr("y", height - 20)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "12px")
    .text("Trade Date");

  if (training_inputs.includes("Training Benchmark") | training_inputs.includes("Training QL")){
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


function _40(htl){return(
htl.html`     <pre>     <h2>  Testing Data Graph </pre>`
)}

function _testing_inputs(Inputs){return(
Inputs.checkbox(["Testing QL", "Testing Benchmark"], {label: "Select Features:"})
)}

function _chart9(d3,width,height,x9,y9,testing_inputs,datasetesting,include_sentiment,xAxis9,yAxis9)
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
  if (testing_inputs.includes("Testing QL")) {
    line9 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.QL));

    path9 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line9(datasetesting));
    const leg1_shape = svg.append("circle").attr("cx",100).attr("cy",20).attr("r", 6).style("fill", "blue")
    const leg1_text = svg.append("text").attr("x", 110).attr("y", 20).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Q Learner").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line10 = d3.line()
  var path10 = svg.append("path")
  if (testing_inputs.includes("Testing Benchmark")) {
    line10 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.benchmark + 500000));

    path10 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "orange")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line10(datasetesting));
    const leg1_shape = svg.append("circle").attr("cx",100).attr("cy",40).attr("r", 6).style("fill", "orange")
    const leg1_text = svg.append("text").attr("x", 110).attr("y", 40).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Benchmark").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  if (testing_inputs.includes("Testing Benchmark")) {
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
    const leg3_shape = svg.append("circle").attr("cx",100).attr("cy",60).attr("r", 6).style("fill", "#00ff00")
    const leg3_text = svg.append("text").attr("x", 110).attr("y", 60).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Buy").style("font-size", "13px").attr("alignment-baseline","middle")

    const leg4_shape = svg.append("circle").attr("cx",100).attr("cy",80).attr("r", 6).style("fill", "#ff0000")
    const leg4_text = svg.append("text").attr("x", 110).attr("y", 80).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Sell").style("font-size", "13px").attr("alignment-baseline","middle")
  }
  
 //DYNAMIC TITLE (W or W/O SENTIMENT ANALYSIS
  if (include_sentiment) {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Testing Data Graph Using Sentiment Data");
  }
  else {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Testing Data Graph Without Using Sentiment Data");
  }
  //AXIS LABEL
  const y_axis_label = svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y",0)
      .attr("x",-180)
      .attr("transform", "rotate(-90)")
      .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
      .style("font-size", "12px")
      .text("Portfolio Value USD");
  
    //AXIS LABEL
  const x_axis_label = svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width - 550)
    .attr("y", height - 6)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "12px")
    .text("Trade Date");
  
  const gx = svg.append("g")
      .call(xAxis9, zx);

  const gy = svg.append("g")
      .call(yAxis9, zy);

  if (testing_inputs.includes("Testing QL") | testing_inputs.includes("Testing Benchmark")){
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


function _43(htl){return(
htl.html`<p>  </p>`
)}

function _44(htl){return(
htl.html`     <pre>     <h1>  Price and Bollinger Band Graph </pre>`
)}

function _inchart1(Inputs){return(
Inputs.toggle({label: "Load Bollinger Band Graph"})
)}

function _bbg_inputs(Inputs){return(
Inputs.checkbox(["Bollinger Band Upper", "Bollinger Band Lower", "Bollinger SMA", "ADJ Close", "SMA"], {label: "Select Features:"})
)}

function _chart(d3,width,height,x,y,bbg_inputs,data,include_sentiment,xAxis,yAxis,inchart1)
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

    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",20).attr("r", 6).style("fill", "blue")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 20).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Bollinger Band Upper").style("font-size", "13px").attr("alignment-baseline","middle")
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

   const leg2_shape = svg.append("circle").attr("cx",1000).attr("cy",40).attr("r", 6).style("fill", "red")
   const leg2_text = svg.append("text").attr("x", 1010).attr("y", 40).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Bollinger Band Lower").style("font-size", "13px").attr("alignment-baseline","middle")
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
    
    const leg3_shape = svg.append("circle").attr("cx",1000).attr("cy",60).attr("r", 6).style("fill", "purple")
    const leg3_text = svg.append("text").attr("x", 1010).attr("y", 60).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Bollinger SMA").style("font-size", "13px").attr("alignment-baseline","middle")
  
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
    
    const leg4_shape = svg.append("circle").attr("cx",1000).attr("cy",80).attr("r", 6).style("fill", "green")
    const leg4_text = svg.append("text").attr("x", 1010).attr("y", 80).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Adjusted Close").style("font-size", "13px").attr("alignment-baseline","middle")
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

    const leg5_shape = svg.append("circle").attr("cx",1000).attr("cy",100).attr("r", 6).style("fill", "black")
    const leg5_text = svg.append("text").attr("x", 1010).attr("y", 100).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Simple Moving Average").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  const tooltip = svg.append("g")
      .style("pointer-events", "none");


  //AXIS LABEL
  const y_axis_label = svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y",20)
      .attr("x",-180)
      .attr("transform", "rotate(-90)")
      .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
      .style("font-size", "12px")
      .text("Price USD");
  
    //AXIS LABEL
  const x_axis_label = svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width - 550)
    .attr("y", height - 6)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "12px")
    .text("Trade Date");

   //DYNAMIC TITLE (W or W/O SENTIMENT ANALYSIS
  if (include_sentiment) {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Bollinger Band Graph Using Sentiment Data");
  }
  else {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Bollinger Band Graph Without Using Sentiment Data");
  }
    
  //TRANSITIONING AXIS
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


function _48(htl){return(
htl.html`<p>  </p>`
)}

function _49(htl){return(
htl.html`     <pre>     <h1>  Bollinger Percentage Graph </pre>`
)}

function _include6(Inputs){return(
Inputs.toggle({label: "Load Bollinger Band % Graph"})
)}

function _chart2(d3,width,height,x,y2,include6,data,include_sentiment,xAxis,yAxis2)
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

     // const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",20).attr("r", 6).style("fill", "purple")
     // const leg1_text = svg.append("text").attr("x", 1010).attr("y", 20).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Bollinger Band Percentage").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line62 = d3.line()
  var path62 = svg.append("path")
  if (include6 == 1) {
    line62 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(0));

    path62 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "red")
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
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line63(data));

    // const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",40).attr("r", 6).style("fill", "blue")
    // const leg1_text = svg.append("text").attr("x", 1010).attr("y", 40).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Bollinger Band Percentage").style("font-size", "13px").attr("alignment-baseline","middle")
  }
    //AXIS LABEL
  const y_axis_label = svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y",20)
      .attr("x",-180)
      .attr("transform", "rotate(-90)")
      .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
      .style("font-size", "12px")
      .text("Bollinger Percentage");
  
    //AXIS LABEL
  const x_axis_label = svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width - 550)
    .attr("y", height - 6)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "12px")
    .text("Trade Date");

  //DYNAMIC TITLE (W or W/O SENTIMENT ANALYSIS
  if (include_sentiment) {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Bollinger Percentage Graph Using Sentiment Data");
  }
  else {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Bollinger Percentage Graph Without Using Sentiment Data");
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


function _52(htl){return(
htl.html`<p>  </p>`
)}

function _53(htl){return(
htl.html`     <pre>     <h1>  Stochastic Oscillator Graph </pre>`
)}

function _include7(Inputs){return(
Inputs.toggle({label: "Load Stochastic Oscillator Graph"})
)}

function _chart3(d3,width,height,x,y3,include7,data,so_ul,so_ll,include_sentiment,xAxis,yAxis3)
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
    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",20).attr("r", 6).style("fill", "purple")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 20).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Stochastic Osciallator").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line72 = d3.line()
  var path72 = svg.append("path")
  if (include7 == 1) {
    line72 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(so_ul));

    path72 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line72(data));
   const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",40).attr("r", 6).style("fill", "blue")
   const leg1_text = svg.append("text").attr("x", 1010).attr("y", 40).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("SO Upper Limit").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line73 = d3.line()
  var path73 = svg.append("path")
  if (include7 == 1) {
    line73 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(so_ll));

    path73 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "Red")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line73(data));

    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",60).attr("r", 6).style("fill", "red")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 60).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("SO Lower Limit").style("font-size", "13px").attr("alignment-baseline","middle")
  }
    //AXIS LABEL
  const y_axis_label = svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y",20)
      .attr("x",-180)
      .attr("transform", "rotate(-90)")
      .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
      .style("font-size", "12px")
      .text("Stochastic Oscillator");
  
    //AXIS LABEL
  const x_axis_label = svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width - 550)
    .attr("y", height - 6)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "12px")
    .text("Trade Date");

   //DYNAMIC TITLE (W or W/O SENTIMENT ANALYSIS
  if (include_sentiment) {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Stochastic Oscillator Graph Using Sentiment Data");
  }
  else {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Stochastic Oscillator Graph Without Using Sentiment Data");
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


function _56(htl){return(
htl.html`<p>  </p>`
)}

function _57(htl){return(
htl.html`     <pre>     <h1>  Price to SMA Ratio Graph </pre>`
)}

function _include8(Inputs){return(
Inputs.toggle({label: "Load Price to SMA Ratio Graph"})
)}

function _chart4(d3,width,height,x,y4,include8,data,smathreshold,xAxis,yAxis4,include_sentiment)
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

    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",20).attr("r", 6).style("fill", "purple")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 20).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Price To SMA Ratio").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line81 = d3.line()
  var path81 = svg.append("path")
  if (include8 == 1) {
    line81 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(smathreshold));

    path81 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line81(data));

    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",40).attr("r", 6).style("fill", "blue")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 40).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Upper Threshold").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line82 = d3.line()
  var path82 = svg.append("path")
  if (include8 == 1) {
    line82 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(-1*smathreshold));

    path82 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line82(data));

    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",60).attr("r", 6).style("fill", "red")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 60).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Lower Threshold").style("font-size", "13px").attr("alignment-baseline","middle")
  }
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis4, zy);

    //AXIS LABEL
  const y_axis_label = svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y",20)
      .attr("x",-180)
      .attr("transform", "rotate(-90)")
      .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
      .style("font-size", "12px")
      .text("Ratio");

  
    //AXIS LABEL
  const x_axis_label = svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width - 550)
    .attr("y", height - 6)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "12px")
    .text("Trade Date");

 //DYNAMIC TITLE (W or W/O SENTIMENT ANALYSIS
  if (include_sentiment) {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Price to SMA Ratio Graph Using Sentiment Data");
  }
  else {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Price to SMA Ratio Graph Without Using Sentiment Data");
  }
  
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


function _60(htl){return(
htl.html`<p>  </p>`
)}

function _61(htl){return(
htl.html`     <pre>     <h1>  Momentum  Graph</pre>`
)}

function _include9(Inputs){return(
Inputs.toggle({label: "Load Momentum Graph"})
)}

function _chart5(d3,width,height,x,y5,include9,data,momentumth,xAxis,yAxis5,include_sentiment)
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

    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",20).attr("r", 6).style("fill", "purple")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 20).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Momentum").style("font-size", "13px").attr("alignment-baseline","middle")
    
  }

  var line91 = d3.line()
  var path91 = svg.append("path")
  if (include9 == 1) {
    line91 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(momentumth));

    path91 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line91(data));

    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",40).attr("r", 6).style("fill", "blue")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 40).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Upper Threshold").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line92 = d3.line()
  var path92 = svg.append("path")
  if (include9 == 1) {
    line92 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(-1*momentumth));

    path92 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line92(data));

    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",60).attr("r", 6).style("fill", "red")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 60).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Lower Threshold").style("font-size", "13px").attr("alignment-baseline","middle")
  }
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis5, zy);

    //AXIS LABEL
  const y_axis_label = svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y",20)
      .attr("x",-180)
      .attr("transform", "rotate(-90)")
      .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
      .style("font-size", "12px")
      .text("Momentum");

  
  const x_axis_label = svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width - 550)
    .attr("y", height - 6)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "12px")
    .text("Trade Date");

   //DYNAMIC TITLE (W or W/O SENTIMENT ANALYSIS
  if (include_sentiment) {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Momentum Graph Using Sentiment Data");
  }
  else {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Momentum Graph Without Using Sentiment Data");
  }
  
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


function _64(htl){return(
htl.html`<p>  </p>`
)}

function _65(htl){return(
htl.html`     <pre>     <h1>  Sentiment Graph</pre>`
)}

function _include10(Inputs){return(
Inputs.toggle({label: "Load Sentiment Graph"})
)}

function _chart6(d3,width,height,x,y6,include10,data,sentimentth,include_sentiment,xAxis,yAxis6)
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
    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",300).attr("r", 6).style("fill", "purple")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 300).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Sentiment Value").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line102 = d3.line()
  var path102 = svg.append("path")
  if (include10 == 1) {
    line102 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(-1*sentimentth));

    path102 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line102(data));
    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",340).attr("r", 6).style("fill", "red")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 340).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Lower Threshold").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line103 = d3.line()
  var path103 = svg.append("path")
  if (include10 == 1) {
    line103 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(sentimentth));

    path103 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "blue")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line103(data));
    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",320).attr("r", 6).style("fill", "blue")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 320).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("Upper Threshold").style("font-size", "13px").attr("alignment-baseline","middle")
  }

   //DYNAMIC TITLE (W or W/O SENTIMENT ANALYSIS
  if (include_sentiment) {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("Sentiment Graph Using Sentiment Data");
  }
  else {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("NOTE: INCLUDE SENTIMENT DATA MUST BE TOGGLED ON FOR THIS GRAPH");
  }
  
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis6, zy);
  //AXIS LABEL
  const y_axis_label = svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y",20)
      .attr("x",-180)
      .attr("transform", "rotate(-90)")
      .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
      .style("font-size", "12px")
      .text("Sentiment Value [-1,1]");
  
    //AXIS LABEL
  const x_axis_label = svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width - 550)
    .attr("y", height - 6)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "12px")
    .text("Trade Date");
  
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


function _68(htl){return(
htl.html`<p>  </p>`
)}

function _69(htl){return(
htl.html`     <pre>     <h1>  MACD Graph </pre>`
)}

function _include11(Inputs){return(
Inputs.toggle({label: "Load MACD Graph (MACD indicator must be toggled on)", value: false})
)}

function _macd_inputs(Inputs){return(
Inputs.checkbox(["MACD", "MACD Signal", "MACD Raw"], {label: "Select Features:"})
)}

function _chart7(d3,width,height,x,y7,macd_inputs,data,xAxis,yAxis7,include_sentiment,include11)
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
  if (macd_inputs.includes("MACD")) {
    line11 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.MACD));

    path11 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "purple")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line11(data));
    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",20).attr("r", 6).style("fill", "purple")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 20).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("MACD").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line112 = d3.line()
  var path112 = svg.append("path")
  if (macd_inputs.includes("MACD Signal")) {
    line112 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.MACD_raw));

    path112 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "green")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line112(data));
    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",40).attr("r", 6).style("fill", "green")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 40).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("MAC Signal").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line113 = d3.line()
  var path113 = svg.append("path")
  if (macd_inputs.includes("MACD Raw")) {
    line113 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(+d.MACD_signal));

    path113 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "brown")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line113(data));
    const leg1_shape = svg.append("circle").attr("cx",1000).attr("cy",60).attr("r", 6).style("fill", "brown")
    const leg1_text = svg.append("text").attr("x", 1010).attr("y", 60).attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; }).text("MACD Raw").style("font-size", "13px").attr("alignment-baseline","middle")
  }

  var line114 = d3.line()
  var path114 = svg.append("path")
  if (macd_inputs.includes("MACD")) {
    line114 = d3.line()
      .x(d => zx(d.TradeDate))
      .y(d => zy(0));

    path114 = svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "black")
      .attr("stroke-width", 1)
      .attr("stroke-miterlimit", 1)
      .attr("d", line114(data));
  }
  
  const gx = svg.append("g")
      .call(xAxis, zx);

  const gy = svg.append("g")
      .call(yAxis7, zy);

    //DYNAMIC TITLE (W or W/O SENTIMENT ANALYSIS
  if (include_sentiment) {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("MACD Graph Using Sentiment Data");
  }
  else {
  const sentiment_label = svg.append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", width - 350)
    .attr("y", 35)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "15px")
    .attr("font-weight",function(d,i) {return 700;})
    .text("MACD Graph Without Using Sentiment Data");
  }

  //AXIS LABEL
  const y_axis_label = svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y",20)
      .attr("x",-180)
      .attr("transform", "rotate(-90)")
      .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
      .style("font-size", "12px")
      .text("MACD");
  
    //AXIS LABEL
  const x_axis_label = svg.append("text")
    .attr("class", "x label")
    .attr("text-anchor", "end")
    .attr("x", width - 550)
    .attr("y", height - 6)
    .attr("font-family", function(d,i) {return i<5 ? "serif" : "sans-serif"; })
    .style("font-size", "12px")
    .text("Trade Date");
   
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


function _73(htl){return(
htl.html`<p>  </p>`
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

function _dataset2(rf,qlgs,url,url2)
{
  if (rf){
    if (qlgs == "Run QLearner"){
      return fetch(url).then(response => response.json()).then(function(data) {return data})
    } else if (qlgs == "Run GridSearch")
      return fetch(url2).then(response => response.json()).then(function(data) {return data})
  }
}


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

function _x(d3,data,margin,width){return(
d3.scaleUtc()
    .domain(d3.extent(data, d => d.TradeDate))
    .range([margin.left, width - margin.right])
)}

function _xAxis(x,height,margin,d3,width){return(
(g, scale = x) => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(scale).ticks(width / 80).tickSizeOuter(0))
)}

function _y(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([0, d3.max(data, d => +d.bollinger_band_upper)])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis(margin,d3,y,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _y6(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([d3.min(data, d => +d.avg_compound_sentiment), d3.max(data, d => +d.avg_compound_sentiment)])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis4(margin,d3,y4,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y4).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _height(){return(
480
)}

function _yAxis2(margin,d3,y2,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y2).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _y4(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([d3.min(data, d => +d.price_to_SMA_ratio), d3.max(data, d => +d.price_to_SMA_ratio)])
    .range([height - margin.bottom, margin.top])
)}

function _min_macd(d3,data){return(
d3.min([d3.min(data, function(d) { return +d.MACD; }), d3.min(data, function(d) { return +d.MACD_signal; }), d3.min(data, function(d) { return +d.MACD_raw; })])
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

function _margin(){return(
{top: 60, right: 30, bottom: 50, left: 70}
)}

function _datasettraining(data){return(
data.filter(d => d.test_or_train == 'train')
)}

function _data2(data){return(
data.map(d => d.momentum)
)}

function _max_y(d3,datasettraining){return(
d3.max([d3.max(datasettraining, function(d) { return +d.QL; }), d3.max(datasettraining, function(d) { return +d.benchmark; })])
)}

function _min_y(d3,datasettraining){return(
d3.min([d3.min(datasettraining, function(d) { return +d.QL; }), d3.min(datasettraining, function(d) { return +d.benchmark; })])
)}

function _97(d3,datasettraining){return(
d3.extent(datasettraining, d => d.TradeDate)
)}

function _x8(d3,datasettraining,margin,width){return(
d3.scaleUtc()
    .domain(d3.extent(datasettraining, d => d.TradeDate))
    .range([margin.left, width - margin.right])
)}

function _max_macd(d3,data){return(
d3.max([d3.max(data, function(d) { return +d.MACD; }), d3.max(data, function(d) { return +d.MACD_signal; }), d3.max(data, function(d) { return +d.MACD_raw; })])
)}

function _y8(d3,min_y,max_y,height,margin){return(
d3.scaleLinear()
    .domain([min_y,max_y])
    .range([height - margin.bottom, margin.top])
)}

function _yAxis5(margin,d3,y5,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y5).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _xAxis8(height,margin,d3,x8,width){return(
g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x8).ticks(width / 80).tickSizeOuter(0))
)}

function _yAxis8(margin,d3,y8,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y8).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _orderstraining(data){return(
data.filter(d => ((d.test_or_train == 'train') & (d.orders == 'BUY' | d.orders == 'BUY')))
)}

function _orderstraining2(orderstraining){return(
orderstraining.map(d => [d.TradeDate, d.orders])
)}

function _y5(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([d3.min(data, d => +d.momentum), d3.max(data, d => +d.momentum)])
    .range([height - margin.bottom, margin.top])
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

function _yAxis7(margin,d3,y7,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y7).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _114(d3,datasetesting){return(
d3.extent(datasetesting, d => d.TradeDate)
)}

function _yAxis6(margin,d3,y6,height){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y6).ticks(height / 40))
    .call(g => g.select(".domain").remove())
)}

function _xAxis9(height,margin,d3,x9,width){return(
g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x9).ticks(width / 80).tickSizeOuter(0))
)}

function _update(chart,timeframe){return(
chart.update(timeframe)
)}

function _y2(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([d3.min(data, d => +d.bollinger_band_percentage), d3.max(data, d => +d.bollinger_band_percentage)])
    .range([height - margin.bottom, margin.top])
)}

function _y7(d3,min_macd,max_macd,height,margin){return(
d3.scaleLinear()
    .domain([min_macd,max_macd])
    .range([height - margin.bottom, margin.top])
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

function _isDataLoaded(dataset2){return(
function isDataLoaded(d) {
  return  dataset2 == undefined
}
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], _1);
  main.variable(observer()).define(["htl"], _2);
  main.variable(observer()).define(["htl"], _3);
  main.variable(observer()).define(["md"], _4);
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
  main.variable(observer()).define(["htl"], _27);
  main.variable(observer()).define(["htl"], _28);
  main.variable(observer("viewof qlgs")).define("viewof qlgs", ["Inputs"], _qlgs);
  main.variable(observer("qlgs")).define("qlgs", ["Generators", "viewof qlgs"], (G, _) => G.input(_));
  main.variable(observer("viewof rf")).define("viewof rf", ["Inputs"], _rf);
  main.variable(observer("rf")).define("rf", ["Generators", "viewof rf"], (G, _) => G.input(_));
  main.variable(observer()).define(["htl"], _31);
  main.variable(observer()).define(["htl"], _32);
  main.variable(observer("viewof dateone")).define("viewof dateone", ["Inputs","training_startdate"], _dateone);
  main.variable(observer("dateone")).define("dateone", ["Generators", "viewof dateone"], (G, _) => G.input(_));
  main.variable(observer("viewof datetwo")).define("viewof datetwo", ["Inputs","testing_enddate"], _datetwo);
  main.variable(observer("datetwo")).define("datetwo", ["Generators", "viewof datetwo"], (G, _) => G.input(_));
  main.variable(observer()).define(["htl"], _35);
  main.variable(observer()).define(["htl"], _36);
  main.variable(observer()).define(["htl"], _37);
  main.variable(observer("viewof training_inputs")).define("viewof training_inputs", ["Inputs"], _training_inputs);
  main.variable(observer("training_inputs")).define("training_inputs", ["Generators", "viewof training_inputs"], (G, _) => G.input(_));
  main.variable(observer("chart8")).define("chart8", ["d3","width","height","x8","y8","training_inputs","datasettraining","include_sentiment","xAxis8","yAxis8"], _chart8);
  main.variable(observer()).define(["htl"], _40);
  main.variable(observer("viewof testing_inputs")).define("viewof testing_inputs", ["Inputs"], _testing_inputs);
  main.variable(observer("testing_inputs")).define("testing_inputs", ["Generators", "viewof testing_inputs"], (G, _) => G.input(_));
  main.variable(observer("chart9")).define("chart9", ["d3","width","height","x9","y9","testing_inputs","datasetesting","include_sentiment","xAxis9","yAxis9"], _chart9);
  main.variable(observer()).define(["htl"], _43);
  main.variable(observer()).define(["htl"], _44);
  main.variable(observer("viewof inchart1")).define("viewof inchart1", ["Inputs"], _inchart1);
  main.variable(observer("inchart1")).define("inchart1", ["Generators", "viewof inchart1"], (G, _) => G.input(_));
  main.variable(observer("viewof bbg_inputs")).define("viewof bbg_inputs", ["Inputs"], _bbg_inputs);
  main.variable(observer("bbg_inputs")).define("bbg_inputs", ["Generators", "viewof bbg_inputs"], (G, _) => G.input(_));
  main.variable(observer("chart")).define("chart", ["d3","width","height","x","y","bbg_inputs","data","include_sentiment","xAxis","yAxis","inchart1"], _chart);
  main.variable(observer()).define(["htl"], _48);
  main.variable(observer()).define(["htl"], _49);
  main.variable(observer("viewof include6")).define("viewof include6", ["Inputs"], _include6);
  main.variable(observer("include6")).define("include6", ["Generators", "viewof include6"], (G, _) => G.input(_));
  main.variable(observer("chart2")).define("chart2", ["d3","width","height","x","y2","include6","data","include_sentiment","xAxis","yAxis2"], _chart2);
  main.variable(observer()).define(["htl"], _52);
  main.variable(observer()).define(["htl"], _53);
  main.variable(observer("viewof include7")).define("viewof include7", ["Inputs"], _include7);
  main.variable(observer("include7")).define("include7", ["Generators", "viewof include7"], (G, _) => G.input(_));
  main.variable(observer("chart3")).define("chart3", ["d3","width","height","x","y3","include7","data","so_ul","so_ll","include_sentiment","xAxis","yAxis3"], _chart3);
  main.variable(observer()).define(["htl"], _56);
  main.variable(observer()).define(["htl"], _57);
  main.variable(observer("viewof include8")).define("viewof include8", ["Inputs"], _include8);
  main.variable(observer("include8")).define("include8", ["Generators", "viewof include8"], (G, _) => G.input(_));
  main.variable(observer("chart4")).define("chart4", ["d3","width","height","x","y4","include8","data","smathreshold","xAxis","yAxis4","include_sentiment"], _chart4);
  main.variable(observer()).define(["htl"], _60);
  main.variable(observer()).define(["htl"], _61);
  main.variable(observer("viewof include9")).define("viewof include9", ["Inputs"], _include9);
  main.variable(observer("include9")).define("include9", ["Generators", "viewof include9"], (G, _) => G.input(_));
  main.variable(observer("chart5")).define("chart5", ["d3","width","height","x","y5","include9","data","momentumth","xAxis","yAxis5","include_sentiment"], _chart5);
  main.variable(observer()).define(["htl"], _64);
  main.variable(observer()).define(["htl"], _65);
  main.variable(observer("viewof include10")).define("viewof include10", ["Inputs"], _include10);
  main.variable(observer("include10")).define("include10", ["Generators", "viewof include10"], (G, _) => G.input(_));
  main.variable(observer("chart6")).define("chart6", ["d3","width","height","x","y6","include10","data","sentimentth","include_sentiment","xAxis","yAxis6"], _chart6);
  main.variable(observer()).define(["htl"], _68);
  main.variable(observer()).define(["htl"], _69);
  main.variable(observer("viewof include11")).define("viewof include11", ["Inputs"], _include11);
  main.variable(observer("include11")).define("include11", ["Generators", "viewof include11"], (G, _) => G.input(_));
  main.variable(observer("viewof macd_inputs")).define("viewof macd_inputs", ["Inputs"], _macd_inputs);
  main.variable(observer("macd_inputs")).define("macd_inputs", ["Generators", "viewof macd_inputs"], (G, _) => G.input(_));
  main.variable(observer("chart7")).define("chart7", ["d3","width","height","x","y7","macd_inputs","data","xAxis","yAxis7","include_sentiment","include11"], _chart7);
  main.variable(observer()).define(["htl"], _73);
  main.variable(observer("timeframe")).define("timeframe", ["dateone","datetwo"], _timeframe);
  main.variable(observer("datep")).define("datep", ["d3"], _datep);
  main.variable(observer("params")).define("params", ["datep","training_startdate","training_enddate","testing_startdate","testing_enddate","smawindow","bbwindow","bbstdev","so_window","so_window_sma","obv","macd","include_sentiment","mom_window","alpha","gamma","rar","radr","smathreshold","so_ul","so_ll","momentumth","sentimentth"], _params);
  main.variable(observer("dataset2")).define("dataset2", ["rf","qlgs","url","url2"], _dataset2);
  main.variable(observer("cleanedData")).define("cleanedData", ["dataset2"], _cleanedData);
  main.variable(observer("data")).define("data", ["cleanedData"], _data);
  main.variable(observer("x")).define("x", ["d3","data","margin","width"], _x);
  main.variable(observer("xAxis")).define("xAxis", ["x","height","margin","d3","width"], _xAxis);
  main.variable(observer("y")).define("y", ["d3","data","height","margin"], _y);
  main.variable(observer("yAxis")).define("yAxis", ["margin","d3","y","height"], _yAxis);
  main.variable(observer("y6")).define("y6", ["d3","data","height","margin"], _y6);
  main.variable(observer("yAxis4")).define("yAxis4", ["margin","d3","y4","height"], _yAxis4);
  main.variable(observer("height")).define("height", _height);
  main.variable(observer("yAxis2")).define("yAxis2", ["margin","d3","y2","height"], _yAxis2);
  main.variable(observer("y4")).define("y4", ["d3","data","height","margin"], _y4);
  main.variable(observer("min_macd")).define("min_macd", ["d3","data"], _min_macd);
  main.variable(observer("y3")).define("y3", ["d3","data","height","margin"], _y3);
  main.variable(observer("yAxis3")).define("yAxis3", ["margin","d3","y3","height"], _yAxis3);
  main.variable(observer("margin")).define("margin", _margin);
  main.variable(observer("datasettraining")).define("datasettraining", ["data"], _datasettraining);
  main.variable(observer("data2")).define("data2", ["data"], _data2);
  main.variable(observer("max_y")).define("max_y", ["d3","datasettraining"], _max_y);
  main.variable(observer("min_y")).define("min_y", ["d3","datasettraining"], _min_y);
  main.variable(observer()).define(["d3","datasettraining"], _97);
  main.variable(observer("x8")).define("x8", ["d3","datasettraining","margin","width"], _x8);
  main.variable(observer("max_macd")).define("max_macd", ["d3","data"], _max_macd);
  main.variable(observer("y8")).define("y8", ["d3","min_y","max_y","height","margin"], _y8);
  main.variable(observer("yAxis5")).define("yAxis5", ["margin","d3","y5","height"], _yAxis5);
  main.variable(observer("xAxis8")).define("xAxis8", ["height","margin","d3","x8","width"], _xAxis8);
  main.variable(observer("yAxis8")).define("yAxis8", ["margin","d3","y8","height"], _yAxis8);
  main.variable(observer("orderstraining")).define("orderstraining", ["data"], _orderstraining);
  main.variable(observer("orderstraining2")).define("orderstraining2", ["orderstraining"], _orderstraining2);
  main.variable(observer("y5")).define("y5", ["d3","data","height","margin"], _y5);
  main.variable(observer("datasetesting")).define("datasetesting", ["data"], _datasetesting);
  main.variable(observer("max_y2")).define("max_y2", ["d3","datasetesting"], _max_y2);
  main.variable(observer("min_y2")).define("min_y2", ["d3","datasetesting"], _min_y2);
  main.variable(observer("y9")).define("y9", ["d3","min_y2","max_y2","height","margin"], _y9);
  main.variable(observer("yAxis9")).define("yAxis9", ["margin","d3","y9","height"], _yAxis9);
  main.variable(observer("x9")).define("x9", ["d3","datasetesting","margin","width"], _x9);
  main.variable(observer("yAxis7")).define("yAxis7", ["margin","d3","y7","height"], _yAxis7);
  main.variable(observer()).define(["d3","datasetesting"], _114);
  main.variable(observer("yAxis6")).define("yAxis6", ["margin","d3","y6","height"], _yAxis6);
  main.variable(observer("xAxis9")).define("xAxis9", ["height","margin","d3","x9","width"], _xAxis9);
  main.variable(observer("update")).define("update", ["chart","timeframe"], _update);
  main.variable(observer("y2")).define("y2", ["d3","data","height","margin"], _y2);
  main.variable(observer("y7")).define("y7", ["d3","min_macd","max_macd","height","margin"], _y7);
  main.variable(observer("update2")).define("update2", ["chart2","timeframe"], _update2);
  main.variable(observer("update3")).define("update3", ["chart3","timeframe"], _update3);
  main.variable(observer("update4")).define("update4", ["chart4","timeframe"], _update4);
  main.variable(observer("update5")).define("update5", ["chart5","timeframe"], _update5);
  main.variable(observer("update6")).define("update6", ["chart6","timeframe"], _update6);
  main.variable(observer("update7")).define("update7", ["chart7","timeframe"], _update7);
  main.variable(observer("update8")).define("update8", ["chart8","timeframe"], _update8);
  main.variable(observer("update9")).define("update9", ["chart9","timeframe"], _update9);
  main.variable(observer("queryString")).define("queryString", ["params"], _queryString);
  main.variable(observer("url")).define("url", ["queryString"], _url);
  main.variable(observer("url2")).define("url2", ["queryString"], _url2);
  const child1 = runtime.module(define1);
  main.import("howto", child1);
  main.variable(observer("isDataLoaded")).define("isDataLoaded", ["dataset2"], _isDataLoaded);
  return main;
}
