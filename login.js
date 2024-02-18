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
	$.post("192.168.0.135:8000/users/addUser",
		{
			email: document.getElementById("signEmail").value,
			username: "placeholder to allow send",
			password: document.getElementById("signPassword").value
		},
		function(data,status){
			alert("Data: " + data + "\nStatus: " + status);
		});
} 


function sendLoginData() {
	$.post("192.168.0.135:8000/users/loginUser",
		{
			email: document.getElementById("logEmail").value,
			username: "placeholder to allow send",
			password: document.getElementById("logPassword").value
		},
		function(data,status){
			alert("Data: " + data + "\nStatus: " + status);
		});
} 

