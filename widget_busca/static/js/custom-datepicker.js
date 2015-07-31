$(document).ready(function(){

	var now = new Date();
	// Setando tempo todo pra zero para considerar apenas a data.
	now.setHours(0, 0, 0, 0);

	var entrada = $('.datepicker#data_entrada').datepicker({
		format: 'dd/mm/yyyy',
		/*onRender: function(date){
			// Desabilitando todas as datas anteriores a hoje.
			return date.valueOf() < now.valueOf() ? 'disabled' : '';
		}*/
	}).on('changeDate', function(ev){
		// Caso a nova data de entrada selecionada seja maior do que a data de saida.
		if(ev.date.valueOf() > saida.date.valueOf()){
			// Definimos a data de saída como sendo um dia após a nova data de entrada.
			var newDate = new Date(ev.date);
			newDate.setDate(newDate.getDate() + 1);
			saida.setValue(newDate);
		}
		// Escondemos o tooltip do datepicker.
		entrada.hide();
		// Damos foco ao datepicker da data de saída.
		$('.datepicker#data_saida').focus();
	}).data('datepicker');

	var saida = $('.datepicker#data_saida').datepicker({
		format: 'dd/mm/yyyy',
		onRender: function(date){
			// Desabilitando todas as datas menores ou iguais à data de entrada.
			return date.valueOf() <= entrada.date.valueOf() ? 'disabled': '';
		}
	}).on('changeDate', function(ev){
		// Escondendo o tooltip do datepicker.
		saida.hide();
	}).data('datepicker');
});