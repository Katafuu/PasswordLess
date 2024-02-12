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



function Check() {
	var uname = document.getElementById("uname").value;
	var pwd = document.getElementById("logPwd").value;
	const test = fetch("http://192.168.0.135:8000/");
	
} 

