$(document).ready(function(){
	
	// Variables
	var clickedTab = $(".tabs > .active");
	var tabWrapper = $(".tab__content");
	var activeTab = tabWrapper.find(".active");
	var activeTabHeight = activeTab.outerHeight();
	
	// Show tab on page load
	activeTab.show();
	
	// Set height of wrapper on page load
	tabWrapper.height(activeTabHeight);
	
	$(".tabs > li").on("click", function() {
		
		// Remove class from active tab
		$(".tabs > li").removeClass("active");
		
		// Add class active to clicked tab
		$(this).addClass("active");
		
		// Update clickedTab variable
		clickedTab = $(".tabs .active");
		
		// fade out active tab
		activeTab.fadeOut(250, function() {
			
			// Remove active class all tabs
			$(".tab__content > li").removeClass("active");
			
			// Get index of clicked tab
			var clickedTabIndex = clickedTab.index();

			// Add class active to corresponding tab
			$(".tab__content > li").eq(clickedTabIndex).addClass("active");
			
			// update new active tab
			activeTab = $(".tab__content > .active");
			
			// Update variable
			activeTabHeight = activeTab.outerHeight();
			
			// Animate height of wrapper to new tab height
			tabWrapper.stop().delay(50).animate({
				height: activeTabHeight
			}, 500, function() {
				
				// Fade in active tab
				activeTab.delay(50).fadeIn(250);
				
			});
		});
	});
	
	// Variables

	var chart    = document.getElementById('chart1').getContext('2d'),

	gradient = chart.createLinearGradient(0, 0, 0, 900);
	gradient.addColorStop(0, 'rgba( 50, 250, 50, 0.32)');
	gradient.addColorStop(0.3, 'rgba( 50, 250, 50, 0.1)');
	gradient.addColorStop(1, 'rgba( 50, 250, 50, 0)');



	var data  = {
		//labels: [ 'January', 'February', 'March', 'April', 'May', 'June', 'July','August','September','October', 'November','December' ],
		labels: [ 1,2,3,4,5,6,7,8,9,10,11,12],
		datasets: [{
				label: 'Price',
				backgroundColor: gradient,
				pointBackgroundColor: '##89f58f',
				borderWidth: 2,
				borderColor: '#0a8c05',
				data: [20, 45, 40, 30, 35, 55,75,80,40,50,80,50],
				lineAtIndex: 4
			}]
	};

	var options = {
		responsive: true,
		maintainAspectRatio: true,
		animation: {
			easing: 'easeInOutQuad',
			duration: 520
		},
		scales: {
			yAxes: [{
		ticks: {
			fontColor: '#5e6a81'
		},
				gridLines: {
					color: 'rgba(200, 200, 200, 0.08)',
					lineWidth: 1
				}
			}],
		xAxes:[{
		ticks: {
			fontColor: '#5e6a81'
		}
		}]
		},
		elements: {
			line: {
				tension: 0.4
			}
		},
		legend: {
			display: false
		},
		point: {
			backgroundColor: '#00c7d6'
		},
		tooltips: {
			titleFontFamily: 'Poppins',
			backgroundColor: 'rgba(0,0,0,0.4)',
			titleFontColor: 'white',
			caretSize: 5,
			cornerRadius: 2,
			xPadding: 10,
			yPadding: 10
		},
		annotation:{
			annotations:[{
				type:"line",
				mode:"vertical",
				value: 4,
				borderColor: "red",
			}]
		},
		plugins: {
			arbitraryLine: {
			  lineColor: 'red',
			  xPosition: 4,
			},
		}

	};

	var chartInstance = new Chart(chart, {
		type: 'line',
		data: data,
		options: options,
		lineAtIndex: [2,4,8],
	});



	var chart    = document.getElementById('chart').getContext('2d'),

	gradient = chart.createLinearGradient(0, 0, 0, 900);
	gradient.addColorStop(0, 'rgba( 250, 50, 50, 0.32)');
	gradient.addColorStop(0.3, 'rgba( 250, 50, 50, 0.1)');
	gradient.addColorStop(1, 'rgba( 250, 50, 50, 0)');

    gradient2 = chart.createLinearGradient(0, 0, 0, 900);
	gradient2.addColorStop(0, 'rgba(0, 199, 214, 0.32)');
	gradient2.addColorStop(0.3, 'rgba(0, 199, 214, 0.1)');
	gradient2.addColorStop(1, 'rgba(0, 199, 214, 0)');



	var data  = {
		labels: [ 'January', 'February', 'March', 'April', 'May', 'June', 'July','August','September','October', 'November','December' ],
		datasets: [{
				label: 'Applications',
				backgroundColor: gradient,
				pointBackgroundColor: '#00c7d6',
				borderWidth: 2,
				borderColor: '#961205',
				data: [60, 45, 80, 30, 35, 55,25,80,40,50,80,50]
			},
			{
				label: 'Applications2',
				backgroundColor: gradient2,
				pointBackgroundColor: '#e8b4d6',
				borderWidth: 2,
				borderColor: '#331ab1',
				data: [120, 45, 80, 50, 35, 70,25,80,60,50,80,100]
			}]
	};

	var options = {
		responsive: true,
		maintainAspectRatio: true,
		animation: {
			easing: 'easeInOutQuad',
			duration: 520
		},
		scales: {
			yAxes: [{
		ticks: {
			fontColor: '#5e6a81'
		},
				gridLines: {
					color: 'rgba(200, 200, 200, 0.08)',
					lineWidth: 1
				}
			}],
		xAxes:[{
		ticks: {
			fontColor: '#5e6a81'
		}
		}]
		},
		elements: {
			line: {
				tension: 0.4
			}
		},
		legend: {
			display: false
		},
		point: {
			backgroundColor: '#00c7d6'
		},
		tooltips: {
			titleFontFamily: 'Poppins',
			backgroundColor: 'rgba(0,0,0,0.4)',
			titleFontColor: 'white',
			caretSize: 5,
			cornerRadius: 2,
			xPadding: 10,
			yPadding: 10
		}
	};

	var chartInstance = new Chart(chart, {
		type: 'line',
		data: data,
			options: options
	});





	var colorButton = $(".colors li");
	
	colorButton.on("click", function(){
		
		// Remove class from currently active button
		$(".colors > li").removeClass("active-color");
		
		// Add class active to clicked button
		$(this).addClass("active-color");
		
		// Get background color of clicked
		var newColor = $(this).attr("data-color");
		
		// Change background of everything with class .bg-color
		$(".bg-color").css("background-color", newColor);
		
		// Change color of everything with class .text-color
		$(".text-color").css("color", newColor);
	});
});