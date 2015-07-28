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
		property: "name"
	});
});