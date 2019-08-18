input = $('#id_username')

function valid_user(all_users) {
	for (var i = 0; i < all_users.length; i++) {
		if (input.val() == all_users[i]) {
			$("#button_form").prop('disabled', " ")
			$("#error_usr").html("Пользователь с таким логином уже зарегистрирован")
			break;
		} else {
			$("#button_form").prop('disabled', "")
			$("#error_usr").html("")
		}

	}
}