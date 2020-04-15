// World representation
var data = [{
	type:'scattergeo', 
	mode:'markers', 
	locations:['CZE','GBR','DEU','GEO','KOR','FRA','SAU','LVA','POL','HKG','USA','ITA','NOR','LTU','CHE','RUS','BLR','TWN','ISR','TUR','HUN','IRL','EST','ESP','ROU','NZL','AUS','MLT','CHN','THA','ZAF','FIN','MEX','SGP','DNK','GRC','IDN','NLD','MKD','BEL','LIE','SWE','MYS','ARG','URY','IND','BRA','UKR','CAN','JPN','AUT'], 
	marker:{
		reversescale:true, 
		size:[2,18,45,1,2,16,1,1,3,1,107,2,1,1,3,6,1,2,1,1,1,2,1,2,2,1,3,1,157,1,1,2,1,7,1,1,1,10,1,1,1,4,1,1,1,2,2,1,9,4,1], 
		color:[1,6,19,1,1,10,1,1,2,1,56,1,1,1,2,3,1,1,1,1,1,2,1,2,1,1,2,1,100,1,1,1,1,5,1,1,1,7,1,1,1,3,1,1,1,2,1,1,6,3,1], 
		cmin:0, 
		cmax:100, 
		colorscale:'Greens', 
		colorbar:{
			title:'Peers Concentration',
			ticksuffix:'(% max)',
			showticksuffix:'last'
		}, 
		line:{
			color:'black'
		}
	}, 
	name:'peers data'
}];
	
var layout = {
	'geo':{
		'scope':'world', 
		'resolution':50
	}
};

Plotly.newPlot('world',data,layout);


// Pie chart representation
var data2 = [{
	type:"pie", 
	labels:["Czechia","United Kingdom","Germany","Georgia","South Korea","France","Saudi Arabia","Latvia","Poland","Hong Kong SAR China","United States","Italy","Norway","Lithuania","Switzerland","Russia","Belarus","Taiwan","Israel","Turkey","Hungary","Ireland","Estonia","Spain","Romania","New Zealand","Australia","Malta","China","Thailand","South Africa","Finland","Mexico","Singapore","Denmark","Greece","Indonesia","Netherlands","Macedonia","Belgium","Liechtenstein","Sweden","Malaysia","Argentina","Uruguay","India","Brazil","Ukraine","Canada","Japan","Austria"], 
	values:[3,38,119,1,3,59,1,2,9,4,355,5,1,3,10,18,3,4,1,1,1,7,2,7,5,3,10,1,642,3,1,5,1,27,1,3,3,41,1,1,1,14,2,2,2,7,5,3,38,17,1],
	textinfo:"percent",
	textposition:"inside",
	automargin:true
}]

var layout2 = {
	height:400,
	width:400,
	margin:{
		"t":0,
		"b":0,
		"l":0,
		"r":0
	},
	showLegend:false
}

Plotly.newPlot('tester',data2,layout2)


// General stats
document.getElementById("gen-stats-list").innerHTML = "<ul><li><b>Total Peers:</b> 2112</li><li><b>Addresses collisions:</b> 688</li><li><b>Ipv4 peers:</b> 2112</li><li><b>Ipv6 peers:</b> 0</li><li><b>UDP peers:</b> 0</li><li><b>TCP peers:</b> 2112</li><li><b>Number of CID v.0:</b> 1554</li><li><b>Number of CID v.1:</b> 558</li><li><b>Number of outgoing connections:</b> 1993</li><li><b>Number of incoming connections:</b> 119</li><li><b>Number of KAD peers:</b> 2037</li><li><b>Number of BitSwap peers:</b> 95</li><li><b>Number of Fast peers:</b> 1523</li><li><b>Number of Ok peers:</b> 391</li><li><b>Number of Slow peers:</b> 54</li><li><b>Number of unknown latency peers:</b> 144</li><li><b>Number of relayed peers:</b> 96</li><li><b>Average latency (ms):</b> 292</li><li><b>Churn (%):</b> 1</li></ul>"


// Cartesian graph
var newPeers = {
	name:'New Peers',
	x:[0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5,15.0,15.5,16.0,16.5,17.0,17.5,18.0,18.5,19.0,19.5,20.0,20.5,21.0,21.5,22.0,22.5,23.0,23.5,24.0,24.5,25.0,25.5,26.0,26.5,27.0,27.5,28.0,28.5,29.0,29.5,30.0,30.5,31.0,31.5,32.0,32.5,33.0,33.5,34.0,34.5,35.0,35.5,36.0,36.5,37.0,37.5,38.0,38.5,39.0,39.5,40.0,40.5,41.0,41.5,42.0,42.5,43.0,43.5,44.0,44.5,45.0,45.5,46.0,46.5,47.0,47.5,48.0,48.5,49.0,49.5,50.0,50.5,51.0,51.5,52.0,52.5,53.0,53.5,54.0,54.5,55.0,55.5,56.0,56.5,57.0,57.5,58.0,58.5],
	y:[31,81,74,58,55,55,48,30,55,32,63,45,54,34,25,38,38,41,41,34,31,26,25,3,2,1,8,0,3,0,0,4,2,2,2,4,1,0,0,1,1,2,5,0,0,1,1,0,4,3,4,1,1,1,1,39,41,41,47,32,24,57,12,31,31,30,36,36,28,30,37,21,17,16,35,19,22,7,0,2,2,1,0,1,2,2,0,1,3,1,3,0,2,0,0,1,1,1,3,2,2,12,18,20,24,35,34,19,22,18,17,24,23,27,28,0,0],
	mode:'lines+markers',
	type:'scatter'
};

var totPeers = {
	name:'Tot Peers',
	x:[0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5,15.0,15.5,16.0,16.5,17.0,17.5,18.0,18.5,19.0,19.5,20.0,20.5,21.0,21.5,22.0,22.5,23.0,23.5,24.0,24.5,25.0,25.5,26.0,26.5,27.0,27.5,28.0,28.5,29.0,29.5,30.0,30.5,31.0,31.5,32.0,32.5,33.0,33.5,34.0,34.5,35.0,35.5,36.0,36.5,37.0,37.5,38.0,38.5,39.0,39.5,40.0,40.5,41.0,41.5,42.0,42.5,43.0,43.5,44.0,44.5,45.0,45.5,46.0,46.5,47.0,47.5,48.0,48.5,49.0,49.5,50.0,50.5,51.0,51.5,52.0,52.5,53.0,53.5,54.0,54.5,55.0,55.5,56.0,56.5,57.0,57.5,58.0,58.5],
	y:[31,89,126,155,186,214,210,204,232,234,261,261,278,281,105,165,209,232,253,270,265,284,97,91,95,89,93,87,91,86,87,98,106,76,80,81,79,79,72,79,84,75,81,73,69,64,67,65,79,72,73,68,68,69,70,133,175,211,245,245,255,298,91,128,168,220,240,260,254,277,292,122,168,186,214,224,229,208,196,187,180,167,162,157,157,149,144,142,150,142,144,126,126,121,118,119,120,117,118,113,115,151,193,194,229,243,253,252,264,280,300,146,185,213,245,1,0],
	mode:'lines+markers',
	type:'scatter'
};

var avgPeers = {
	name:'Avg Peers',
	x:[0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5,15.0,15.5,16.0,16.5,17.0,17.5,18.0,18.5,19.0,19.5,20.0,20.5,21.0,21.5,22.0,22.5,23.0,23.5,24.0,24.5,25.0,25.5,26.0,26.5,27.0,27.5,28.0,28.5,29.0,29.5,30.0,30.5,31.0,31.5,32.0,32.5,33.0,33.5,34.0,34.5,35.0,35.5,36.0,36.5,37.0,37.5,38.0,38.5,39.0,39.5,40.0,40.5,41.0,41.5,42.0,42.5,43.0,43.5,44.0,44.5,45.0,45.5,46.0,46.5,47.0,47.5,48.0,48.5,49.0,49.5,50.0,50.5,51.0,51.5,52.0,52.5,53.0,53.5,54.0,54.5,55.0,55.5,56.0,56.5,57.0,57.5,58.0,58.5],
	y:[31,60,82,100,117,133,144,151,160,168,176,183,190,197,191,189,190,192,196,199,202,206,201,197,193,189,185,182,178,175,172,170,168,165,163,161,158,156,154,152,151,149,147,146,144,142,140,139,138,136,135,134,133,131,130,130,131,132,134,136,138,141,140,140,140,141,143,144,146,148,150,150,150,150,151,152,153,154,154,155,155,155,155,155,155,155,155,155,155,155,155,154,154,154,153,153,152,152,152,151,151,151,151,152,153,153,154,155,156,157,159,158,159,159,160,159,157],
	mode:'lines',
	type:'scatter'
};

var layout3={
	xaxis:{
		title:{
			text:'Hours',
			font:{
				family:'Courier New,monospace',
				size: 18,
				color: '#7f7f7f'
			}
		},
	},
	yaxis: {
		title:{
			text:'Number of Peers',
			font:{
				family: 'Courier New,monospace',
				size: 18,
				color: '#7f7f7f'
			}
		}
	}
}

var graphData=[newPeers,totPeers,avgPeers];

Plotly.newPlot('graph',graphData,layout3);
