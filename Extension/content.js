

function checkField(name){
  const field = document.querySelector('input[type*='+name+']'); // the * indicates it is looking for one instance of the args[0] value within the query. https://www.w3.org/TR/selectors/#attribute-substrings
  console.log('field found first')
  if (!field){
    console.log("reached field missing")
    field = document.getElementById(name); // extra checks added to maximise chances of finding it
    if (!field) {
      field = document.getElementsByName(name);
    } 
    else{
      console.log(field)
      return field
    };
  } 
  else {
    console.log(field)
    return field
  };
};

function findField(standardNames) {
  const field = null;
  const count = 0;
  while(!field && count < length(standardNames)) {
    field = checkField(standardNames[count]);
    count++;
  };
  return field
};

const resptest = chrome.runtime.sendMessage({rq:'token'});

function main() {
  chrome.runtime.sendMessage({rq:'token'})
  .then(function(token) {
    console.log(token); // json error. idk how to process response
    const pwd_field = findField(['password','password-field','pwd','user_password']);
    console.log(pwd_field)
    if (pwd_field) {
      const url = document.baseURI;
      console.log(url)
      const options = {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer '+token
        }
      }; 
      console.log(options)
      fetch("https://passwordless.duckdns.org/creds/getCred?siteurl="+url,options)
      .then(data => data.json)
      .then(function(data){
        if (data) {
          const email_field = findField(['email']);
          const uname_field = findField(['username','name']);
          pwd_field.innerText = data.password;
          uname_field.innerText = data.username;
          email_field.innerText = data.email;
        } 
        else {
          // to add popup to save code here w/event listener
          console.log("No saved credential found: "+data);
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






