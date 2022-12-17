$(document).ready(function() {

	// Set the token so that we are not rejected by server
	var csrf_token = $('meta[name=csrf-token]').attr('content');
	 // Configure ajaxSetup so that the CSRF token is added to the header of every request
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrf_token);
	        }
	    }
	});

	$("a.vote").on("click", function() {
		var clicked_obj = $(this);

		// Which idea was clicked? Which button?
		var idea_id = $(this).attr('id');
		var vote_type = $(this).children()[0].id;

		$.ajax({
			url: '/vote',
			type: 'POST',
			data: JSON.stringify({ idea_id: idea_id, vote_type: vote_type}),
			contentType: "application/json; charset=utf-8",
        	dataType: "json",
			success: function(response){
				console.log(response);

				// Update the html rendered to reflect new count
				// Check which count to update
				if(vote_type == "up") {
					clicked_obj.children()[1].innerHTML = " " + response.upvotes;
				} else {
					clicked_obj.children()[1].innerHTML = " " + response.downvotes;
				}
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
