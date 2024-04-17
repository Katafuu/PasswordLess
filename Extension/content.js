function checkField(name){
  let field = document.querySelector('input[type*='+name+']'); // the * indicates it is looking for one instance of the args[0] value within the query. https://www.w3.org/TR/selectors/#attribute-substrings
  console.log('checking Type '+name)
  if (!field){
    console.log("checking ID: "+name)
    field = document.querySelector('input[id*='+name+']'); // extra checks added to maximise chances of finding it
    if (!field) {
      console.log('checking Name '+name)
      field = document.querySelector('input[name*='+name+']');
      if (!field) {
        console.log(name+ " FIELD NOT FOUND")
        console.log('-----')
        return null
      }
      else {
        console.log(name+ " FIELD FOUND: "+field)
        return field
      }
    } 
    else{
      console.log(name+ " FIELD FOUND: "+field)
      return field
    };
  } 
  else {
    console.log(name+ " FIELD FOUND: "+field)
    return field
  };
};

function findFieldFromNames(standardNames) {
  var field = null;
  var count = 0;
  while(!field && count < standardNames.length) {
    field = checkField(standardNames[count]);
    count++;
  };
  return field
};

function main() {
  chrome.runtime.sendMessage({rq:'token'})
  .then(function(token) {
    console.log(token); // json error. idk how to process response
    const pwd_field = findFieldFromNames(['password','password-field','pwd','user_password']);
    console.log(pwd_field)
    if (pwd_field) {
      const url = window.location.origin;
      console.log(url)
      const options = {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer '+token
        }
      }; 
      console.log(options)
      fetch("https://passwordless.duckdns.org:8000/creds/getCred?siteurl="+url,options)
      .then(function(data){
        if (data.status == 200) {
          data = data.json()
          const email_field = findFieldFromNames(['email','logEmail']);
          const uname_field = findFieldFromNames(['signName','username','name']);
          pwd_field.value = data.password;;
          uname_field.value = data.username;
          email_field.value = data.email;;
        } 
        else {
          // to add popup to save code here w/event listener
          alert("No saved credential found");
        };
      });
    }
  })
}

if (document.readyState !== 'loading') {
  main()
}
else {
  document.addEventListener("DOMContentLoaded", function(){
    main()
  })
}






