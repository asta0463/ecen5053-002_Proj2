$(document).ready(function(){
	
	$('input[type=radio][name=unit]').on('change', function(){
	$("#temp_unit").text($(this).val());
	$("#temp_unit1").text($(this).val());
	$("#temp_unit2").text($(this).val());
	$("#temp_unit3").text($(this).val());
	$("#temp_unit4").text($(this).val());
	});
	 
	
    $("#btn1").click(function(){
        var unitCF = $('#unit:checked').val(); 
		$("#test1").text(unitCF);
    });
    $("#btn2").click(function(){
        $("#test2").html("<b>Hello world!</b>");
    });
    $("#btn3").click(function(){
        $("#test3").val("Dolly Duck");
    });
});
