var paymentSign="$";function otherPayment(){var e=document.getElementById("choices-payment-currency").value;paymentSign=e,document.getElementsByClassName("product-line-price").forEach(function(e){isUpdate=e.value.slice(1),e.value=paymentSign+isUpdate}),recalculateCart()}var isPaymentEl=document.getElementById("choices-payment-currency"),choices=new Choices(isPaymentEl,{searchEnabled:!1});function isData(){var e=document.getElementsByClassName("plus"),t=document.getElementsByClassName("minus");e&&e.forEach(function(n){n.onclick=function(e){var t;parseInt(n.previousElementSibling.value)<10&&(e.target.previousElementSibling.value++,e=n.parentElement.parentElement.previousElementSibling.querySelector(".product-price").value,t=n.parentElement.parentElement.nextElementSibling.querySelector(".product-line-price"),updateQuantity(n.parentElement.querySelector(".product-quantity").value,e,t))}}),t&&t.forEach(function(n){n.onclick=function(e){var t;1<parseInt(n.nextElementSibling.value)&&(e.target.nextElementSibling.value--,e=n.parentElement.parentElement.previousElementSibling.querySelector(".product-price").value,t=n.parentElement.parentElement.nextElementSibling.querySelector(".product-line-price"),updateQuantity(n.parentElement.querySelector(".product-quantity").value,e,t))}})}document.querySelector("#profile-img-file-input").addEventListener("change",function(){var e=document.querySelector(".user-profile-image"),t=document.querySelector(".profile-img-file-input").files[0],n=new FileReader;n.addEventListener("load",function(){e.src=n.result},!1),t&&n.readAsDataURL(t)}),flatpickr("#date-field",{enableTime:!0,dateFormat:"d M, Y, h:i K"}),isData();var count=1;function new_link(){count++;var e=document.createElement("tr"),t=(e.id=count,e.className="product",'<tr><th scope="row" class="product-id">'+count+'</th><td class="text-start"><div class="mb-2"><input class="form-control bg-light border-0" type="text" id="shippingTaxno" placeholder="Product Name"></div><textarea class="form-control bg-light border-0" id="shippingAddress" rows="2" placeholder="Product Details"></textarea></div></td><td><input class="form-control bg-light border-0 product-price" type="number" placeholder="$0.00"></td><td><div class="input-step"><button type="button" class="minus">–</button><input type="number" class="product-quantity" value="0" readonly><button type="button" class="plus">+</button></div></td><td class="text-end"><div><input type="text" class="form-control bg-light border-0 product-line-price" placeholder="$0.00" /></div></td><td class="product-removal"><a class="btn btn-success">Delete</a></td></tr'),n=(e.innerHTML=document.getElementById("newForm").innerHTML+t,document.getElementById("newlink").appendChild(e),document.querySelectorAll("[data-trigger]"));for(i=0;i<n.length;++i){var a=n[i];new Choices(a,{placeholderValue:"This is a placeholder set in the config",searchPlaceholderValue:"This is a search placeholder"})}isData(),remove(),amountKeyup(),resetRow()}remove();var taxRate=.125,shippingRate=65,discountRate=.15;function remove(){document.querySelectorAll(".product-removal a").forEach(function(e){e.addEventListener("click",function(e){removeItem(e),resetRow()})})}function resetRow(){document.getElementById("newlink").querySelectorAll("tr").forEach(function(e,t){t+=1;e.querySelector(".product-id").innerHTML=t})}function recalculateCart(){var t=0,e=(document.getElementsByClassName("product").forEach(function(e){e.getElementsByClassName("product-line-price").forEach(function(e){e.value&&(t+=parseFloat(e.value.slice(1)))})}),t*taxRate),n=t*discountRate,a=0<t?shippingRate:0,l=t+e+a-n;document.getElementById("cart-subtotal").value=paymentSign+t.toFixed(2),document.getElementById("cart-tax").value=paymentSign+e.toFixed(2),document.getElementById("cart-shipping").value=paymentSign+a.toFixed(2),document.getElementById("cart-total").value=paymentSign+l.toFixed(2),document.getElementById("cart-discount").value=paymentSign+n.toFixed(2),document.getElementById("totalamountInput").value=paymentSign+l.toFixed(2),document.getElementById("amountTotalPay").value=paymentSign+l.toFixed(2)}function amountKeyup(){document.getElementsByClassName("product-price").forEach(function(n){n.addEventListener("keyup",function(e){var t=n.parentElement.nextElementSibling.nextElementSibling.querySelector(".product-line-price");updateQuantity(e.target.value,n.parentElement.nextElementSibling.querySelector(".product-quantity").value,t)})})}function updateQuantity(e,t,n){e=(e=e*t).toFixed(2);n.value=paymentSign+e,recalculateCart()}function removeItem(e){e.target.closest("tr").remove(),recalculateCart()}amountKeyup();var genericExamples=document.querySelectorAll("[data-trigger]");for(i=0;i<genericExamples.length;++i){var element=genericExamples[i];new Choices(element,{placeholderValue:"This is a placeholder set in the config",searchPlaceholderValue:"This is a search placeholder"})}function billingFunction(){document.getElementById("same").checked?(document.getElementById("shippingName").value=document.getElementById("billingName").value,document.getElementById("shippingAddress").value=document.getElementById("billingAddress").value,document.getElementById("shippingPhoneno").value=document.getElementById("billingPhoneno").value,document.getElementById("shippingTaxno").value=document.getElementById("billingTaxno").value):(document.getElementById("shippingName").value="",document.getElementById("shippingAddress").value="",document.getElementById("shippingPhoneno").value="",document.getElementById("shippingTaxno").value="")}!function(){"use strict";window.addEventListener("load",function(){var e=document.getElementsByClassName("needs-validation");Array.prototype.filter.call(e,function(t){t.addEventListener("submit",function(e){!1===t.checkValidity()&&(e.preventDefault(),e.stopPropagation()),t.classList.add("was-validated")},!1)})},!1)}();var cleaveBlocks=new Cleave("#cardNumber",{blocks:[4,4,4,4],uppercase:!0}),genericExamples=document.querySelectorAll('[data-plugin="cleave-phone"]');for(i=0;i<genericExamples.length;++i){element=genericExamples[i];new Cleave(element,{delimiters:["(",")","-"],blocks:[0,3,3,4]})}