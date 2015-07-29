$(document).ready(function(){
	$("#busca-cidade-hotel").typeahead({
		/* Procurando apenas depois de termos digitado 3 letras. Isso economizará requisições ao servidor. */
		minLength: 3,
		source: function(typeahead, query){
			$.ajax({
				url: "lookup/?q=" + query,
				success: function(data){
					typeahead.process(data);
				}
			});
		},
		property: "name",
		//Redefinindo o evento de selecionar um item do autocomplete
		onselect: function(obj){
			//Colocamos como valor do input o valor do atributo typeahead_name do item.
			$("#busca-cidade-hotel").val(obj['typeahead_name']);
			// Salvamos nos campos hidden o seu id e o seu tipo
			$('input#cidade_hotel_id').val(obj.id)
			$('input#cidade_hotel_type').val(obj.type)
		}
	});
});