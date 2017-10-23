$(document).ready(function(){
	
	$('input[type=radio][name=unit]').on('change', function(){
	$("#temp_unit").text($(this).val());
	$("#temp_unit1").text($(this).val());
	$("#temp_unit2").text($(this).val());
	$("#temp_unit3").text($(this).val());
	$("#temp_unit4").text($(this).val());
	socket.send($(this).val());
	console.log("sending "+$(this).val());
	});
	
	var socket = new WebSocket('ws://192.168.43.185:8080/ws');
	
	socket.onopen = function(){  
	console.log("connected"); 
	$("#temp_unit4").text("Connected")
	};
	
	socket.onopen = function(){  
	console.log("connected"); 
	$("#temp_unit4").text("Disconnected")
	};

// Functions to request the correct data from tornado
		
	$("#cur_data").click(function(){
		socket.send ("cur_data");
		console.log("Get current data");
    });
	
	$("#get_avg_temp").click(function(){
		socket.send ("avg_temp");
		console.log("Get average temp");
    });
	
	$("#get_min_temp").click(function(){
		socket.send ("min_temp");
		console.log("Get min temp");
    });
	
	$("#get_max_temp").click(function(){
		socket.send ("max_temp");
		console.log("Get max temp");
    });
	
	$("#get_last_temp").click(function(){
		socket.send ("last_temp");
		console.log("Get last temp");
    });
	
	$("#get_last_hum").click(function(){
		socket.send ("last_hum");
		console.log("Get last humidity");
    });
		
	$("#get_avg_hum").click(function(){
		socket.send ("avg_hum");
		console.log("Get avg hum");
    });		
	
	$("#get_max_hum").click(function(){
		socket.send ("max_hum");
		console.log("Get max humidity");
    });		
	
	$("#get_min_hum").click(function(){
		socket.send ("min_hum");
		console.log("Get min humidity");
    });		
	
// Switch case to call the correct function to update data after response from tornado	
	
	socket.onmessage = function (message) {
	var array = (message.data).split(',');
	console.log("update " + array[0]);
	 switch(array[0]){
       case "cur_data":
            console.log('cur_data');
			update_cur_data(array);
			break;
       case "avg_temp":
            console.log('avg_temp');
			update_avg_temp(array);
			break;
	   case "min_temp":
            console.log('min_temp');
			update_min_temp(array);
			break;
	   case "max_temp":
            console.log('max_temp');
			update_max_temp(array);
			break;
	   case "last_temp":
            console.log('last_temp');
			update_last_temp(array);
			break;	
	   case "last_hum":
            console.log('last_hum');
			update_last_hum(array);
			break;			
	   case "avg_hum":
            console.log('avg_hum');
			update_avg_hum(array);
			break;
	   case "max_hum":
            console.log('max_hum');
			update_max_hum(array);
			break;
	   case "min_hum":
            console.log('min_hum');
			update_min_hum(array);
			break;			
	   default:
            console.log('default')
			
			;break;
    }
	
	};
		

/// Functions for writing data to the right fields in the html page
	
	update_cur_data=function(array){
		console.log("writing: " + 'current data');
		$("#cur_time").text(array[1]);
		//console.log("writing: " + array[1]);
		$("#cur_temp").text(array[2]);
		//console.log("writing: " + array[2]);
		$("#cur_hum").text(array[3]);
		//console.log("writing: " + array[3]);
	}
	
	update_avg_temp=function(array){
		console.log("writing: " + array[0]);
		$("#avg_temp_ts").text(array[1]);
		$("#avg_temp").text(array[2]);
	}
	
	update_max_temp=function(array){
		console.log("writing: " + array[0]);
		$("#max_temp_ts").text(array[1]);
		$("#max_temp").text(array[2]);
	}
	
	update_min_temp=function(array){
		console.log("writing: " + array[0]);
		$("#min_temp_ts").text(array[1]);
		$("#min_temp").text(array[2]);
	}
	
	update_last_temp=function(array){
		console.log("writing: " + array[0]);
		$("#last_temp_ts").text(array[1]);
		$("#last_temp").text(array[2]);
	}
	
	update_last_hum=function(array){
		console.log("writing: " + array[0]);
		$("#last_hum_ts").text(array[1]);
		$("#last_hum").text(array[2]);
	}	
	
	update_avg_hum=function(array){
		console.log("writing: " + array[0]);
		$("#avg_hum_ts").text(array[1]);
		$("#avg_hum").text(array[2]);
	}	

	update_max_hum=function(array){
		console.log("writing: " + array[0]);
		$("#max_hum_ts").text(array[1]);
		$("#max_hum").text(array[2]);
	}	

	update_min_hum=function(array){
		console.log("writing: " + array[0]);
		$("#min_hum_ts").text(array[1]);
		$("#min_hum").text(array[2]);
	}	
	
});
