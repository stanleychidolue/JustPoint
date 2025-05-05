// Start of Cart js Functionalities

// function to get csrf_token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  
  const csrftoken = getCookie('csrftoken');
  
  // Pop over function /////

  document.addEventListener('click',(e)=>{
    if(e.target.parentElement.classList.contains("Airtime")){
      airtime_data_popup = document.querySelector(".popOver");
      if (airtime_data_popup.hasAttribute("hidden")){
      airtime_data_popup.removeAttribute("hidden");
      }else{
        airtime_data_popup.setAttribute("hidden",true);
    }
    }else{
      airtime_data_popup = document.querySelector(".popOver");
    if (airtime_data_popup.hasAttribute("hidden")==false){
      airtime_data_popup.setAttribute("hidden",true);
    }
    }
  })
  
  // function for calling addToCart function to all element with class=add_to_cart in the current page
  let cartAddBtns=document.querySelectorAll(".add_to_cart")
  cartAddBtns.forEach(btn=>{
    btn.addEventListener("click",addToCart)
  })
  
  // function for adding a clicked product to cart
  function addToCart(e){
    let option = e.target.parentElement.value
    let product_id = e.target.id
    let url = window.location.origin+"/cart/add-to-cart/"+option+"/"
    let data = {id:product_id}
  
    fetch(url,{
      method: "POST",
      headers: {'Content-Type':"application/json",'X-CSRFToken': csrftoken},
      body:JSON.stringify(data)
    })
  
    .then(res=>res.json())
    // .then(json => console.log(JSON.stringify(json.item_qty)))
    .then(data=>{
      
                if(data.prod_in_cart){
                  rmFromCart(e);
                }
                else{
                  e.target.src="https://nastpoints3bucket.s3.eu-north-1.amazonaws.com/static/images/cart_activate.svg"
                  e.target.classList.add("cart_activate");
                // sleep(1000).then(() => { e.target.classList.remove("fav_activate"); });
                // document.getElementById('no_of_saved_items').innerHTML=data.num_of_saved_items;
                }
                // sleep(3000).then(() => { e.target.classList.remove("cart_activate");
                //                         e.target.src="https://nastpoints3bucket.s3.eu-north-1.amazonaws.com/static/images/Wheel-cart.svg" });
                document.getElementById('no_of_cart_items').innerHTML=data.num_of_cart_items;
                document.getElementById("quantity"+data.item_prod_id).innerHTML=data.item_qty;
                document.getElementById("total_cart_sum").innerHTML=data.total_cart_sum;
                document.getElementById("total_cart_sum_discount").innerHTML=data.total_cart_sum_disc;
                document.getElementById("total_cart_sum_shipping_fee").innerHTML=data.total_cart_sum_shipping_fee;
                document.getElementById("total_checkout_cost").innerHTML=data.total_checkout_cost;
                try{
                  document.getElementById('main_no_of_cart_items').innerHTML='X'+data.num_of_cart_items;
                  document.getElementById("main_quantity"+data.item_prod_id).innerHTML=data.item_qty;
                  document.getElementById("main_total_cart_sum").innerHTML=data.total_cart_sum;
                  document.getElementById("main_total_cart_sum_discount").innerHTML=data.total_cart_sum_disc;
                  document.getElementById("main_total_cart_sum_shipping_fee").innerHTML=data.total_cart_sum_shipping_fee;
                  document.getElementById("main_total_checkout_cost").innerHTML=data.total_checkout_cost;
                  
                }
                catch{}
  
                
  })
    // .then(data=>{document.getElementById('no_of_cart_items').innerHTML=data}) Note: for single response (include safe=False) 
    
    .catch(error=>{console.log(error)})
  }
  
  // function for calling rmFromCart function to all element with class=rm_from_cart in the current page
  let cartRmvBtns=document.querySelectorAll(".rm_from_cart")
  cartRmvBtns.forEach(btn=>{
    btn.addEventListener("click",rmFromCart)
  })
  // function for removing a clicked product from cart
  function rmFromCart(e){
    // let product_id = e.target.value
    let product_id = e.target.id
    let prod_cart=document.querySelector(".add_to_cart.id_"+product_id)
    let url = window.location.origin+"/cart/rm-from-cart/"
    let data = {id:product_id}
  
    fetch(url,{
      method: "POST",
      headers: {'Content-Type':"application/json",'X-CSRFToken': csrftoken},
      body:JSON.stringify(data)
    })
  
    .then(res=>res.json())
    .then(data=>{
                e.target.src="https://nastpoints3bucket.s3.eu-north-1.amazonaws.com/static/images/Wheel-cart.svg";
                document.getElementById('no_of_cart_items').innerHTML=data.num_of_cart_items;
                if(data.item_qty<1){
                  document.getElementById("item_"+data.item_prod_id).remove();
                  prod_cart.src="https://nastpoints3bucket.s3.eu-north-1.amazonaws.com/static/images/Wheel-cart.svg";
                  try{document.getElementById("main_item_"+data.item_prod_id).remove();}
                  catch{} 
                }
                else{
                  document.getElementById("quantity"+data.item_prod_id).innerHTML=data.item_qty;
                  try{document.getElementById("main_quantity"+data.item_prod_id).innerHTML=data.item_qty;}
                  catch{}
                }
                document.getElementById("total_cart_sum").innerHTML=data.total_cart_sum;
                document.getElementById("total_cart_sum_discount").innerHTML=data.total_cart_sum_disc;
                document.getElementById("total_cart_sum_shipping_fee").innerHTML=data.total_cart_sum_shipping_fee;
                document.getElementById("total_checkout_cost").innerHTML=data.total_checkout_cost;
                try{
                  document.getElementById('main_no_of_cart_items').innerHTML='X'+data.num_of_cart_items;
                  document.getElementById("main_total_cart_sum").innerHTML=data.total_cart_sum;
                  document.getElementById("main_total_cart_sum_discount").innerHTML=data.total_cart_sum_disc;
                  document.getElementById("main_total_cart_sum_shipping_fee").innerHTML=data.total_cart_sum_shipping_fee;
                  document.getElementById("main_total_checkout_cost").innerHTML=data.total_checkout_cost;
                }
                catch{}
  
  })
    .catch(error=>{console.log(error)})
  }
  
  
  
  
  const sleep = function(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  // let closePopUpBtn=document.getElementById("pop_up_close")
  // closePopUpBtn.addEventListener("click",()=>{
  //   document.getElementById("pop_up_container").style.left="-324px"})
  
  
  // function for calling addToFav function to all element with class=add_to_fav in the current page
  let favAddBtns=document.querySelectorAll(".add_to_fav")
  favAddBtns.forEach(btn=>{
    btn.addEventListener("click",addToFav)
  })
  
  // function for adding a clicked product to favourite
  function addToFav(e){
    // let product_id = e.target.value
    let product_id = e.target.id
    let url = window.location.origin+"/customer/add-to-favourite"
    let data = {id:product_id}
    document.getElementById("pop_up_container").style.left="-324px"
  
    fetch(url,{
      method: "POST",
      headers: {'Content-Type':"application/json",'X-CSRFToken': csrftoken},
      body:JSON.stringify(data)
    })
  
  
    .then(res=>res.json())
    .then(data=>{
                if(data.num_of_saved_items==="user_not_authenticated"){
                  document.getElementById("pop_up_container").style.left="24px";
                }
                else if(data.num_of_saved_items==="item_already_saved"){
                  rmFromFav(e);
                }
                else{
                e.target.src="https://nastpoints3bucket.s3.eu-north-1.amazonaws.com/static/images/favourite_activate.svg" 
                e.target.classList.add("fav_activate");
                sleep(1000).then(() => { e.target.classList.remove("fav_activate"); });
                document.getElementById('no_of_saved_items').innerHTML=data.num_of_saved_items;
              }
                
               
  })
    .catch(error=>{console.log(error)})
  }
  
  // function for adding a clicked product to favourite
  let favRmvBtns=document.querySelectorAll(".rm_from_fav")
  favRmvBtns.forEach(btn=>{
    btn.addEventListener("click",rmFromFav)
  })
  
  // function for removing a clicked product to favourite
  function rmFromFav(e){
    // let product_id = e.target.value
    let product_id = e.target.id
    let url = window.location.origin+"/customer/rm-from-favourite"
    let data = {id:product_id}
  
    fetch(url,{
      method: "POST",
      headers: {'Content-Type':"application/json",'X-CSRFToken': csrftoken},
      body:JSON.stringify(data)
    })
  
    .then(res=>res.json())
    .then(data=>{
                e.target.src="https://nastpoints3bucket.s3.eu-north-1.amazonaws.com/static/images/Black-heart.svg";
                document.getElementById('no_of_saved_items').innerHTML=data.num_of_saved_items;
                let favRmvBtns=document.querySelectorAll(".rm_from_fav")
                if(favRmvBtns.length > 0){
                  location.reload()
                }            
  })
    .catch(error=>{console.log(error)})
  }
  
  
  // reloading page when cartIcon is clicked and call cartTab to appear on NavBar
  let loadTab = sessionStorage.getItem("loadTab")
  let cartIcon = document.querySelector('.cartIcon');
  let cartTab = document.querySelector('.cartTab');
  
  // cartIcon.addEventListener("click", () => {
  //   sessionStorage.setItem("loadTab", "true")
  //   location.reload()
  // })
  
  window.onload = () => {
    if(loadTab){
      cartTab.classList.add('showcart')
      // sessionStorage.clear() // This cleans all the session storage
          //  OR
      // If you want to  remove ONLY the item from the storage use:
      sessionStorage.removeItem("loadTab")
    }
  };
  
  
  // password toggle functionality
  const pswToggleBtns=document.querySelectorAll(".psw_toggle")
  
  pswToggleBtns.forEach(btn=>{btn.addEventListener("click",()=>{
    let toggleInput = btn.previousElementSibling
    let eyeIcon = btn.firstChild
    if (toggleInput.type==="password"){
      eyeIcon.classList.remove('bi-eye-fill')
      eyeIcon.classList.add('bi-eye-slash-fill')
      toggleInput.setAttribute("type","text");
    }else{
      eyeIcon.classList.add('bi-eye-fill')
      eyeIcon.classList.remove('bi-eye-slash-fill')
      toggleInput.setAttribute("type","password");
    }
  })})
  
  
  // Responsive Search button
  window.addEventListener('DOMContentLoaded', () => {
  
    let searchBtn = document.querySelector('.searchBtn');
    let closeBtn = document.querySelector('.closeBtn');
    let searchBox = document.querySelector('.searchBox');
    let cartIcon = document.querySelector('.cartIcon');
    let closeCart = document.querySelector('.closeCart');
    let closeCart2= document.querySelector('.body')
    let cartTab = document.querySelector('.cartTab');
    
        searchBtn.onclick = function () {
            searchBox.classList.add('active')
            closeBtn.classList.add('active')
            searchBtn.classList.add('active')
        }
        closeBtn.onclick = function () {
            searchBox.classList.remove('active')
            closeBtn.classList.remove('active')
            searchBtn.classList.remove('active')
        }
        // cartIcon.onclick = function () {
        //     cartTab.classList.add('showcart')
        // }
  
        
        closeCart.onclick = function () {
            cartTab.classList.remove('showcart')
        }
  
        closeCart2.onclick = function () {
          cartTab.classList.remove('showcart')
      }
  
      // Scroll reveal
      const sr = ScrollReveal({
        origin: 'top',
        distance: '40px',
        duration: '2500',
        reset: true
      })
      
      
      // sr.reveal ('.about-container',{beforeReset: function(){sr.sync()},delay:100});
      // sr.reveal ('.product-top',{beforeReset: function(){sr.sync()},delay:200});
      // sr.reveal ('.carousel-inner',{beforeReset: function(){sr.sync()},delay:100});
      // sr.reveal ('.promotion-image',{beforeReset: function(){sr.sync()},delay:100});
      // sr.reveal ('.main-advert',{beforeReset: function(){sr.sync()},delay:100});
  
  
      sr.reveal ('.about-container',{delay:100});
      sr.reveal ('.product-top',{delay:200});
      sr.reveal ('.carousel-inner',{delay:100});
      sr.reveal ('.promotion-image',{delay:100});
      sr.reveal ('.main-advert',{delay:100});
      
      window.addEventListener('load', function() {
      sr.reveal ('.about-container',{delay:100});
      sr.reveal ('.product-top',{delay:200});
      sr.reveal ('.carousel-inner',{delay:100});
      sr.reveal ('.promotion-image',{delay:100});
      sr.reveal ('.main-advert',{delay:100});
      })
      // View Product thumbnail
  
      mainImg = document.getElementById('mainImg');
  
      thumb1 =document.getElementById('thumb1');
      thumb1Src = document.getElementById('thumb1').src;
      thumb2 =document.getElementById('thumb2');
      thumb2Src = document.getElementById('thumb2').src;
      thumb3 =document.getElementById('thumb3');
      thumb3Src = document.getElementById('thumb3').src;
      
      thumb1.addEventListener("click", function() {
        mainImg.src=thumb1Src
      })
      thumb2.addEventListener("click", function() {
        mainImg.src=thumb2Src
      })
      thumb3.addEventListener("click", function() {
        mainImg.src=thumb3Src
      })
  }, false)
  // Navbar disappear
  let prevScrollpos = window.pageYOffset;

  window.addEventListener('scroll', () => {
      
      const header = document.querySelector('header');
  
      let currentScrollPos = window.pageYOffset;
  
      if (prevScrollpos < currentScrollPos && currentScrollPos > "80") {
          header.classList.add('hide');
      } else {
          header.classList.remove('hide');
      }
  
      prevScrollpos = currentScrollPos
  })
  
  
  // Start of single_product quantity selection section
  let inc=document.getElementById("increment")
  let input = document.getElementById("input")
  let inputValue = document.getElementById("input_value")
  let dec=document.getElementById("decrement")
  
  // let counter=inputValue.textContent
  // function increment (){
  //   counter++;
  // }
  
  // function decrement (){
  //   counter--;
  // }
  
  // inc.addEventListener("click",()=>{
  //   increment()
  //   input.value=counter
  //   inputValue.innerHTML=counter
  // })
  
  // dec.addEventListener("click",()=>{
  //   if(counter>0){
  //     decrement()
  //     input.value=counter
  //     inputValue.innerHTML=counter
  //   }
  // })
  // // End of single_product quantity selection section
  
  // Start of single_product size selection section
  
  let sizeBtns= document.querySelectorAll(".size_choice")
  sizeBtns.forEach(btn=>{
    btn.addEventListener('click',sizeSelection)
  })
  
  let sizeInput = document.getElementById("choice_size")
  function sizeSelection(e){
    let value=e.target.textContent
    try{
      let activeSizeBtn=document.querySelector(".activate")
      activeSizeBtn.classList.remove("activate");
    }
    catch{
      
    }
    e.target.classList.add("activate");
    sizeInput.value=value
  }
  
  
  // End of single_product size selection section
  
  
    
  // Collection Nav image change
  
  function changeImg(imgchanger) {
    document.getElementById('slider').src = imgchanger;
  }
  