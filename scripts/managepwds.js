
function addListItem(lstid, data) {
  const vallist = document.getElementById(lstid);

	var newListItem = document.createElement('li');
  var newVal = document.createTextNode(data);
  var newLink = document.createElement('a')
	newLink.setAttribute('href','#')
  newLink.appendChild(newVal);
	newListItem.appendChild(newLink)

  vallist.appendChild(newListItem);
}

function clearList(lstid) {
	const lst = document.getElementById(lstid);
	lst.innerHTML = '';
}


function getCookieToken() {
	let cookies = document.cookie.split(';');
	for(i = 0; i < cookies.length; i++) {
	  cookies[i] = cookies[i].split('=')
	};
	for (x = 0; x < cookies.length; x++){
	  if (cookies[x][0] == 'token') {
		return cookies[x][1];
	  };
	};
  };

function updateCreds() {
	var token = getCookieToken();
	const options = {
		method: 'GET',
		headers: {
				'Content-Type':
						'application/json;charset=utf-8',
				"Authorization": 'Bearer '+token
		}
	};
	fetch("https://passwordless.duckdns.org:8000/users/config", options)
	.then(data => data.json())
	.then(function(data) {
	clearList("credList")
    for (x = 0;x<data.length;x++) {
      addListItem("credList",data[x]);
    }
  });
}

$(document).ready(function(){
	updateCreds()
	});

