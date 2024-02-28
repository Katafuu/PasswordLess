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
		.then(d => {console.log(d)});
		window.location.href = "https://passwordless.duckdns.org/loginsignup.html?created=True"
};

$(document).ready(function () {
  $("loginForm").submit(function (event) {
    var formData = {
      email: document.getElementById("logEmail"),
      password: document.getElementById("logPassword"),
    };

    $.ajax({
      type: "POST",
      url: "https://passwordless.duckdns.org:8000/login",
      data: formData,
      dataType: "json",
      encode: true,
    }).done(function (data) {
      console.log(data);
    });

    event.preventDefault();
  });
});