import {setToken, checkTokenExists} from 'cookie-manager.js'



$(window).on("hashchange", function () {
	if (location.hash.slice(1) == "signup") {
		$(".page").addClass("extend");
		$("#login").removeClass("active");
		$("#signup").addClass("active");
	} else {
		$(".page").removeClass("extend");
		$("#login").addClass("active");
		$("#signup").removeClass("active");
	}
});
$(window).trigger("hashchange");



function sendSignupData() {
	const options = {
		method: 'POST',
		headers: {
				'Content-Type':
						'application/json;charset=utf-8'
		},
		body: JSON.stringify({
			email: document.getElementById("signEmail").value,
			username: document.getElementById("signName").value,
			password: document.getElementById("signPassword").value
		},)
	}
	fetch("https://passwordless.duckdns.org:8000/users/addUser",options)
		.then(res => res.json())
		.then(d => {console.log(d)})
		.then(function(token) {
			setToken(token)
	window.location.href("#login");
});
};

setToken(token)