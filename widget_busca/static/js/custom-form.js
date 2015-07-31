$(document).ready(function(){
	// Toggle do checkbox de periodo indefinido adiciona/remove atributo required das datas.
	// Esse atributo é utilizado pelo validator do bootstrap para validar quais campos são necessários para a submissão do form.
	$('input#periodo_indefinido').click(function(event){
		if($(event.target).is(":checked")){
			$('.datepicker').removeAttr('required');
			$('.datepicker').prop('disabled', true);
		}
		else{
			$('.datepicker').attr('required', true);
			$('.datepicker').prop('disabled', false);
		}
	});
});