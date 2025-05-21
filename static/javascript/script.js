// Start of Cart js Functionalities

// function to get csrf_token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// Pop over function /////

if (window.location.pathname == "/") {
  document.addEventListener("click", (e) => {
    if (e.target.parentElement.classList.contains("Airtime")) {
      airtime_data_popup = document.querySelector(".popOver");
      if (airtime_data_popup.hasAttribute("hidden")) {
        airtime_data_popup.removeAttribute("hidden");
      } else {
        airtime_data_popup.setAttribute("hidden", true);
      }
    } else {
      airtime_data_popup = document.querySelector(".popOver");
      if (airtime_data_popup.hasAttribute("hidden") == false) {
        airtime_data_popup.setAttribute("hidden", true);
      }
    }
  });
}

// Data bundle selelection functionality //
 let bundleOptions= document.querySelectorAll(".bundleOption");

 bundleOptions.forEach(btn => {
  btn.addEventListener("click", (btn)=>{
    let dataOptionsDropdown = document.querySelector(".dataOptionsDropdown");
    dataOptionsDropdown.removeAttribute("hidden");
    document.querySelectorAll(".dataOption").forEach(e=>{e.setAttribute("hidden",true)});  // add hidden attr to all data options //
    bundleOptions.forEach(e=>e.removeAttribute("disabled"));  // add hidden attr to all data options //activeBundleOption
    bundleOptions.forEach(e=>e.classList.remove("activeBundleOption"));  // add hidden attr to all data options //
    let id= btn.target.id;
    btn.target.classList.add("activeBundleOption")
    let selelectedOption=document.querySelectorAll('.'+id);
    selelectedOption.forEach(e =>{e.removeAttribute("hidden");})
  });
  });





   

   let inputsToStop=document.querySelectorAll(".stopEnterSubmit");
   inputsToStop.forEach(e => {
    e.addEventListener('onkeypress',stopSubmit);
    e.addEventListener('keydown',stopSubmit);
    e.addEventListener('keyup',stopSubmit);
   });
  
 if (window.location.pathname.slice(0,17) == "/utility-payment/") {
  //  To detect any changes in the inputs
  let identifierInput = document.querySelector(".identifierInput");
  let subscriptionPlanInput = document.querySelector(".subscriptionPlanInput");
   identifierInput.addEventListener('change',checkUtilityInputs);
   subscriptionPlanInput.addEventListener('change',checkUtilityInputs);
 }


//  function to stop the submision of form with ENTER key
function stopSubmit(e){
  if(e.keyCode === 13){
      e.preventDefault();
      return false
  }
}

//  function to check if all inputs filled and then activating the proceed button
 function checkUtilityInputs(){
  let identifierInput = document.querySelector(".identifierInput");
  let subscriptionPlanInput = document.querySelector(".subscriptionPlanInput");
  if(identifierInput.value != "" && subscriptionPlanInput.value != "" ){
    document.querySelector('.submitCustomerDetailBtn').classList.remove("disabled");
  }
 }


// function for calling addToCart function to all element with class=addToCart in the current page
let cartAddBtns = document.querySelectorAll(".addToCart");
cartAddBtns.forEach((btn) => {
  btn.addEventListener("click", addToCart);
});

// function for adding a clicked product to cart
function addToCart(e) {
  let option = e.target.value;
  let product_id = e.target.id;
  let product_type = e.target.getAttribute("data-product-type");
  let trigger= e.target.getAttribute("data-trigger")
  let url = window.location.origin + "/customer/add-to-cart/" + option + "/";
  let data = { id: product_id, eventTrigger:trigger,product_type:product_type };

  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    // .then(json => console.log(JSON.stringify(json.item_qty)))
    .then((data) => {
      if (data.prod_in_cart ) {
        rmFromCart(e);
      } else {
        if (typeof(trigger) == "string"){
        e.target.classList.remove("bi-cart");
        e.target.classList.add("bi-cart-check-fill","favActivate");
        }
        if (trigger=="button"){e.target.innerHTML="Added"};
        sleep(500).then(() => {
          e.target.classList.remove("favActivate");
        });
        
      }
      
      document.getElementById("no_of_cart_items").innerHTML =
        data.num_of_cart_items;
        if (typeof(trigger) != "string"){
      document.getElementById("quantity" + data.item_prod_id).innerHTML =
        data.item_qty;}
      document.getElementById("total_cart_sum").innerHTML = data.total_cart_sum;
      // document.getElementById("total_cart_sum_discount").innerHTML =
      //   data.total_cart_sum_disc;
      document.getElementById("total_cart_sum_shipping_fee").innerHTML =
        data.total_cart_sum_shipping_fee;
      document.getElementById("total_checkout_cost").innerHTML =
        data.total_checkout_cost;
      try {
        document.getElementById("main_no_of_cart_items").innerHTML =
          "x" + data.num_of_cart_items;
        document.getElementById("main_quantity" + data.item_prod_id).innerHTML =
          data.item_qty;
        document.getElementById("main_total_cart_sum").innerHTML =
          data.total_cart_sum;
        // document.getElementById("main_total_cart_sum_discount").innerHTML =
        //   data.total_cart_sum_disc;
        document.getElementById("main_total_cart_sum_shipping_fee").innerHTML =
          data.total_cart_sum_shipping_fee;
        document.getElementById("main_total_checkout_cost").innerHTML =
          data.total_checkout_cost;
          console.log(data.total_checkout_cost)
      } catch {}
    })
    // .then(data=>{document.getElementById('no_of_cart_items').innerHTML=data}) Note: for single response (include safe=False)

    .catch((error) => {
      console.log(error);
    });
}

// function for calling rmFromCart function to all element with class=rmFromCart in the current page
let cartRmvBtns = document.querySelectorAll(".rmFromCart");
cartRmvBtns.forEach((btn) => {
  btn.addEventListener("click", rmFromCart);
});
// function for removing a clicked product from cart
function rmFromCart(e) {
  // let product_id = e.target.value
  let product_id = e.target.id;
  let prod_cart = document.querySelector(".add_to_cart.id_" + product_id);
  let product_type = e.target.getAttribute("data-product-type");
  let url = window.location.origin + "/customer/rm-from-cart/";
  let trigger= e.target.getAttribute("data-trigger")
  let data = { id: product_id, eventTrigger:trigger, product_type:product_type};

  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((data) => {
      if (trigger=="button"){
        e.target.classList.add("bi-cart-check-fill","favActivate");
        e.target.innerHTML="Added"
      }else{
        if (typeof(trigger) == "string"){
        e.target.classList.add("bi-cart","favActivate");
        e.target.classList.remove("bi-cart-check-fill",);
        }
      }
      
      sleep(500).then(() => {
          e.target.classList.remove("favActivate");
        });
    
      document.getElementById("no_of_cart_items").innerHTML =
        data.num_of_cart_items;
      if (data.item_qty < 1 ) {
        if (typeof(trigger) != "string"){
        document.getElementById("item_" + data.item_prod_id).remove();}
        try {
          document.getElementById("main_item_" + data.item_prod_id).remove();
        } catch {}
      } else {
        document.getElementById("quantity" + data.item_prod_id).innerHTML =
          data.item_qty;
        try {
          document.getElementById(
            "main_quantity" + data.item_prod_id
          ).innerHTML = data.item_qty;
        } catch {}
      }
      document.getElementById("total_cart_sum").innerHTML = data.total_cart_sum;
      // document.getElementById("total_cart_sum_discount").innerHTML =
        data.total_cart_sum_disc;
      document.getElementById("total_cart_sum_shipping_fee").innerHTML =
        data.total_cart_sum_shipping_fee;
      document.getElementById("total_checkout_cost").innerHTML =
        data.total_checkout_cost;
      try {
        document.getElementById("main_no_of_cart_items").innerHTML =
          "x" + data.num_of_cart_items;
        document.getElementById("main_total_cart_sum").innerHTML =
          data.total_cart_sum;
        // document.getElementById("main_total_cart_sum_discount").innerHTML =
        //   data.total_cart_sum_disc;
        document.getElementById("main_total_cart_sum_shipping_fee").innerHTML =
          data.total_cart_sum_shipping_fee;
        document.getElementById("main_total_checkout_cost").innerHTML =
          data.total_checkout_cost;
      } catch {}
    })
    .catch((error) => {
      console.log(error);
    });
}

  
const sleep = function (ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

// delivery fee info

let infoIcons=document.querySelectorAll(".deliveryInquiry");
 infoIcons.forEach(icon => {
    icon.addEventListener("click",()=>{
      let info=document.querySelector(".delivery-inquiry-info")
      if(info.hasAttribute("hidden")){
      info.removeAttribute("hidden")
      }else{
        info.setAttribute("hidden",true)
      }
    })
 });


// closing the favpopinfo
let closePopUpBtn = document.querySelector(".closePopup");
closePopUpBtn.addEventListener("click", () => {
  document.getElementById("favPopupInfo").style.display = "none";
});

// function for calling addToFav function to all element with class=add_to_fav in the current page
let favAddBtns = document.querySelectorAll(".addToFav");
favAddBtns.forEach((btn) => {
  btn.addEventListener("click", addToFav);
});

// function for adding a clicked product to favourite
function addToFav(e) {
  // let product_id = e.target.value
  let id = e.target.id;
  let favType = e.target.getAttribute("data-fav-type");
  let url = "";
  let data = { id: id ,favType:favType};
  if (favType == "estate") {
    url = window.location.origin + "/customer/add-to-estate-favourite/";
  } else if (favType == "product") {
    url = window.location.origin + "/customer/add-to-product-favourite/";
  }
  
  document.getElementById("favPopupInfo").style.display = "none";

  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.message === "user_not_authenticated") {
        document.getElementById("favPopupInfo").style.display = "inline";
      } else if (data.message === "item_already_saved") {
        rmFromFav(e);
      } else {
        e.target.classList.remove("bi-heart");
        e.target.classList.add("bi-heart-fill");
        e.target.classList.add("favActivate");
        sleep(500).then(() => {
          e.target.classList.remove("favActivate");
        });
        // document.getElementById('no_of_saved_items').innerHTML=data.num_of_saved_items;
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

// function for removing a clicked product to favourite
let favRmvBtns = document.querySelectorAll(".rm_from_fav");
favRmvBtns.forEach((btn) => {
  btn.addEventListener("click", rmFromFav);
});

function rmFromFav(e) {
  // let product_id = e.target.value
  let favType = e.target.getAttribute("data-fav-type");
  let id = e.target.id;
  let url = "";
  let data = { id: id ,favType:favType};
  if (favType == "estate") {
    url = window.location.origin + "/customer/rm-from-estate-favourite/";
  } else if (favType == "product") {
    url = window.location.origin + "/customer/rm-from-product-favourite/";
  }

  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((data) => {
      e.target.classList.remove("bi-heart-fill");
      e.target.classList.add("bi-heart");
      e.target.classList.add("favActivate");
      sleep(500).then(() => {
        e.target.classList.remove("favActivate");
      });
      if (window.location.pathname.slice(0, 10) == "/customer/") {
        window.location.reload();
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

let searchInput= document.querySelectorAll(".searchInput");
searchInput.forEach(input => {
  // input.addEventListener('change',searchItem);
  input.addEventListener('input',(e)=>{
    if (e.target.value){
    closeBtn=e.target.nextElementSibling;
    closeBtn.removeAttribute("hidden");
    input.addEventListener("keydown",searchItem);
    input.addEventListener('onkeypress',searchItem);
    input.addEventListener('keyup',searchItem);
    closeBtn.addEventListener("click",(btn)=>{
      e.target.value="";   // To clear the old value
      e.target.focus();    // To put focus on the input as soon as the input old value is cleared
      btn.target.setAttribute("hidden",true);
      searchItem(e);
    });
    
    }else{
      e.target.nextElementSibling.setAttribute("hidden",true);
    }       
    

  })
    
});



function searchItem(e){
  let id = e.target.id;
  let searchLocation = e.target.getAttribute("data-search-loc");
  let lettersTyped = e.target.value;
  let url = window.location.origin + "/products/search/";
  // if (favType == "estate") {
  //   url = window.location.origin + "/customer/add-to-estate-favourite/";
  // } else if (favType == "product") {
  //   url = window.location.origin + "/customer/add-to-product-favourite/";
  // }
  let data = { id: id, searchLocation: searchLocation, lettersTyped:lettersTyped };

  if (lettersTyped != ""){
  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((data) => {
      let searchDropdown=document.querySelector(".searchResultDropdown");
      searchDropdown.removeAttribute("hidden");
      let listcontainer=searchDropdown.firstElementChild;
      listcontainer.innerHTML="";
      if (data.contains.length != 0){
        data.contains.forEach(lookup => {
          let list = document.createElement("li");
          list.classList.add("mt-2","py-1");
          
          if (searchLocation!="products"){
            let listItem = document.createTextNode(lookup);
            let link=document.createElement("a");
            list.classList.add("resultDropdownItem");
            link.setAttribute("href",`/products/shop/${lookup}/`)
            link.classList.add("text-decoration-none","text-dark")
            list.appendChild(listItem)
            link.appendChild(list);
            listcontainer.appendChild(link);
          }else{
          let listItem = document.createTextNode(lookup[0]);
          let cartBtn = document.createElement("button");
          cartBtn.innerHTML="Add to Cart";
          cartBtn.classList.add("ms-sm-4","ms-2","resultDropdownItem",);
          cartBtn.setAttribute("data-trigger","button");
          cartBtn.setAttribute("id",lookup[1]);
          cartBtn.setAttribute("value"," ");
          cartBtn.setAttribute("data-product-type","product");
          
          cartBtn.addEventListener("click", addToCart, {once:true});
          list.appendChild(listItem);
          list.appendChild(cartBtn);
          listcontainer.appendChild(list);
        }
  
        });
      }else{
        // searchDropdown.setAttribute("hidden",true);
        let list = document.createElement("li");
          list.classList.add("resultDropdownItem","pt-2" ,"mb-3");
          let listItem = document.createTextNode("No results found");
          list.appendChild(listItem);
          listcontainer.appendChild(list);
      }
      
    })
    .catch((error) => {
      console.log(error);
    });
  }else{
    let searchDropdown=document.querySelector(".searchResultDropdown");
      searchDropdown.setAttribute("hidden",true);
      let listcontainer=searchDropdown.firstElementChild;
      listcontainer.innerHTML="";
      window.location.reload(true);
  }


}


// reloading page when cartIcon is clicked and call cartTab to appear on NavBar
let loadTab = sessionStorage.getItem("loadTab");
let cartIcon = document.querySelector(".cartIcon");
let cartTab = document.querySelector(".cartTab");

cartIcon.addEventListener("click", () => {
  sessionStorage.setItem("loadTab", "true")
  location.reload()
})

window.onload = () => {
  if (loadTab) {
    cartTab.classList.add("showcart");
    // sessionStorage.clear() // This cleans all the session storage
    //  OR
    // If you want to  remove ONLY the item from the storage use:
    sessionStorage.removeItem("loadTab");
  }
};

// password toggle functionality
const pswToggleBtns = document.querySelectorAll(".psw_toggle");

pswToggleBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    let toggleInput = btn.previousElementSibling;
    let eyeIcon = btn.firstChild;
    if (toggleInput.type === "password") {
      eyeIcon.classList.remove("bi-eye-fill");
      eyeIcon.classList.add("bi-eye-slash-fill");
      toggleInput.setAttribute("type", "text");
    } else {
      eyeIcon.classList.add("bi-eye-fill");
      eyeIcon.classList.remove("bi-eye-slash-fill");
      toggleInput.setAttribute("type", "password");
    }
  });
});





// Responsive Search button
window.addEventListener(
  "DOMContentLoaded",
  () => {
    let searchBtn = document.querySelector(".searchBtn");
    let closeBtn = document.querySelector(".closeBtn");
    let searchBox = document.querySelector(".searchBox");
    let cartIcon = document.querySelector(".cartIcon");
    let closeCart = document.querySelector(".closeCart");
    let closeCart2 = document.querySelector(".body");
    let cartTab = document.querySelector(".cartTab");

    searchBtn.onclick = function () {
      searchBox.classList.add("active");
      closeBtn.classList.add("active");
      searchBtn.classList.add("active");
    };
    closeBtn.onclick = function () {
      searchBox.classList.remove("active");
      closeBtn.classList.remove("active");
      searchBtn.classList.remove("active");
    };
    // cartIcon.onclick = function () {
    //     cartTab.classList.add('showcart')
    // }

    closeCart.onclick = function () {
      cartTab.classList.remove("showcart");
      window.location.reload()
    };

    closeCart2.onclick = function () {
      if (cartTab.classList.contains("showcart")){
      window.location.reload()
      cartTab.classList.remove("showcart");
      }
    };

  },
  false
);



// Navbar disappear
let prevScrollpos = window.pageYOffset;

window.addEventListener("scroll", () => {
  const header = document.querySelector("header");

  let currentScrollPos = window.pageYOffset;

  if (prevScrollpos < currentScrollPos && currentScrollPos > "80") {
    header.classList.add("hide");
  } else {
    header.classList.remove("hide");
  }

  prevScrollpos = currentScrollPos;
});




if (window.location.pathname.slice(0,16) == "/product-details/"){
// Start of single_product quantity selection section
let inc = document.getElementById("increment");
let input = document.getElementById("input");
let dec = document.getElementById("decrement");


inc.addEventListener("click",()=>{
  let counter = document.getElementById("input_value").textContent;
  counter++
  input.value=counter
  inputValue.innerHTML=counter
})

dec.addEventListener("click",()=>{
  if(counter>0){
    let counter = document.getElementById("input_value").textContent;
    counter--
    input.value=counter
    inputValue.innerHTML=counter
  }
})
}
// // End of single_product quantity selection section

// Collection Nav image change
function changeImg(imgchanger) {
  document.getElementById("slider").src = imgchanger;
}
