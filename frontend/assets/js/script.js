let auth0Client = null;


// const fetchAuthConfig = () => fetch("/auth_config.json");


const configureClient = async () => {
    const response = {
    "domain": "dev-vehpzandb3knezrr.us.auth0.com",
    "clientId": "C6c795SScHKdXHRtg4KM6yFJc3A5L3k8"
  };
    const config = response;
  
    auth0Client = await auth0.createAuth0Client({
      domain: config.domain,
      clientId: config.clientId
    });
  };

  // ..

  window.onload = async () => {

    // .. code ommited for brevity
    await configureClient();
  
    updateUI();
  
    const isAuthenticated = await auth0Client.isAuthenticated();
  
    if (isAuthenticated) {
      // show the gated content
      return;
    }
  
    // NEW - check for the code and state parameters
    const query = window.location.search;
    if (query.includes("code=") && query.includes("state=")) {
  
      // Process the login state
      await auth0Client.handleRedirectCallback();
      
      updateUI();
  
      // Use replaceState to redirect the user away and remove the querystring parameters
      window.history.replaceState({}, document.title, "/");
    }
  };
  
  
  // NEW
  const updateUI = async () => {
    const isAuthenticated = await auth0Client.isAuthenticated();
  
    //change text on button to signed in instead of log in
    console.log("Bitch we already logged in")
    // document.getElementById("btn-logout").disabled = !isAuthenticated;
     if(isAuthenticated){
         $('#loginbutton').text('Log Out')
       $('#loginbutton').attr("onclick","logout()")
     }
     
    // document.getElementById("btn-login").disabled = isAuthenticated;
  };


  const login = async () => {
    await auth0Client.loginWithRedirect({
      authorizationParams: {
        redirect_uri: "https://green-basket.vercel.app"
      }
    });
  };

const logout = () => {
  auth0Client.logout({
    logoutParams: {
      returnTo: "https://green-basket.vercel.app"
    }
  });
};