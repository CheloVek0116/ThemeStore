$("#card-image-0").prop('style', ' ');

function readURL(input) {
	var name = input.getAttribute("name")
	if (input.files && input.files[0]) {
		var reader = new FileReader();
		reader.onload = function (e) {
			$('#' + name)
			.attr('src', e.target.result)
			.width(150)
			.height(150);
		};
		reader.readAsDataURL(input.files[0]);
		$("#id_" + name.replace(/images/g, 'preview')).prop('disabled', '');
		$("#" + name.replace(/images/g, 'btn')).prop('disabled', '');
		var index = parseInt(name.match(/[0-9]/)[0]) + 1;
		$("[id='card-image-" + index + "']").prop('style', ' ');
	}
}

function removeIMG(btn_id) {
	$("#" + btn_id).prop('disabled', ' ');
	$("#id_" + btn_id.replace(/btn/g, 'preview')).prop('disabled', ' ');
	$("#id_" + btn_id.replace(/btn/g, 'preview')).prop('checked', false);
	$("#" + btn_id.replace(/btn/g, 'images')).prop('src', '/static/img/no_image.png');
	$("#id_" + btn_id.replace(/btn/g, 'images')).val('');
}

function checked_preview(check) {
	if (!check.checked) {
		check.checked = true
	}
	$('[id$=-preview]').on('click',
		function() {
			$('[id$=-preview]').not($(this)).prop('checked', false);
		}
	);
}
