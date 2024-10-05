
// Wait until the entire page is loaded
window.addEventListener('load', function () {
    // Get the preloader element by its ID
    var preloader = document.getElementById('loadingOverlay');
    
    // Add a fade-out effect
    preloader.style.transition = 'opacity 0.5s ease, visibility 0.5s ease';
    preloader.classList.add('hidden'); // Add the hidden class to hide the preloader
    
    // Optional: You can completely remove the preloader from the DOM after the transition
    setTimeout(function () {
        preloader.style.display = 'none';
    }, 100);  // Match the duration with the transition time (0.5s)
});





//update cart quantity from cart page 
function updateCartqty(productId, action) {
    //   disabled the cart decrease quantity btn 
    const quantityElement = document.getElementById('cart-quantity-' + productId);
    let currentQuantity = parseInt(quantityElement.textContent.trim());

    // Disable the "remove" button if quantity is 1
    const removeButton = document.getElementById('cartqtydec');

    if (action === 'remove' && currentQuantity <= 1) {
        // Do not send the request if the quantity is 1
        removeButton.disabled = true;
        return;  // Exit the function
    }

    // Enable the remove button if quantity is greater than 1
    if (action === 'add') {
        removeButton.disabled = false;
    }





      // Prepare data to send via AJAX
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      let data = new FormData();
      data.append('product', productId);
      if (action === 'remove') {
          data.append('remove', true);
      }
      
      // Send AJAX request
      fetch("/updatecartqty", {
          method: "POST",
          headers: {
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': csrfToken
          },
          body: data
      })
      .then(response => response.json())
      .then(data => {
          if (data.product_id) {
             
              // Update the product's cart quantity in the UI
              const quantityElement = document.getElementById('cart-quantity-' + productId);
              quantityElement.textContent = data.quantity ;
              
  
              // Update the cart length displayed somewhere (e.g., in the navbar)
              const cartLengthElement = document.getElementById('cart-total');
              cartLengthElement.textContent = ' (' + data.cart_length + ')';


              const itemTotalPriceElement = document.getElementById('item-total-' + productId);
              itemTotalPriceElement.textContent = '$' + data.item_total_price.toFixed(2);

         

              // Update the overall cart total price
              const cartTotalPriceElement = document.getElementById('cart-total-price');
              cartTotalPriceElement.textContent = 'Total: $' + data.total_price.toFixed(2);
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
  }






  $(document).ready(function() {
    // Initially hide all sizes
    $(".choose-size").hide();

    // Handle color selection
    $(".choose-color").on('click', function() {
        $(".choose-size").removeClass('active');
        $(".choose-color").removeClass('focused');
        $(this).addClass('focused');

        var selectedColor = $(this).data('color');

        // Show sizes based on selected color
        $(".choose-size").hide();
        $(".color" + selectedColor).show();
        $(".color" + selectedColor).first().addClass('active');

        // Update the price according to the first available size of the selected color
        var firstSizePrice = $(".color" + selectedColor).first().data('price');
        $(".product-price").text("$" + firstSizePrice);
    });

    // Handle size selection and price update
    $(".choose-size").on('click', function() {
        $(".choose-size").removeClass('active');
        $(this).addClass('active');

        var selectedPrice = $(this).data('price');
        $(".product-price").text("$" + selectedPrice);
    });

    // Automatically select the first color and size on page load
    var firstColor = $(".choose-color").first();
    firstColor.addClass('focused');
    var initialColor = firstColor.data('color');
    $(".color" + initialColor).show();
    $(".color" + initialColor).first().addClass('active');
    var initialPrice = $(".color" + initialColor).first().data('price');
    $(".product-price").text("$" + initialPrice);




  // Add to cart
  $('#addToCartbtn').on('click', function() {
    // Get product details
    var _vm=$(this);
    var productId = $("#product_id").val();
    var productTitle = $("#product_title").val();
    var quantity = $("#productqty").val();
    var selectedColor = $(".choose-color.focused").data('color');
    var selectedSize = $(".choose-size.active").text();
    var selectedPrice = $(".product-price").text();
    console.log(productId,productTitle,quantity,selectedColor,selectedSize,selectedPrice);

    // Ajax
    $.ajax({
        url:'/addtocart',
        data:{
            'id':productId,
            'qty':quantity,
            'title':productTitle,
            'price':selectedPrice,
    'color':selectedColor,
    'size':selectedSize
        },
        dataType:'json',
        beforeSend:function(){
            _vm.attr('disabled',true);
        },
        success:function(res){
            $("#cart-total").text(' (' + res.totalitems+ ')');

  window.location.href = "/cart";
  console.log(res)
            _vm.attr('disabled',false);
        }
    });
    // End
   });

  
});


//his is home page and all pages add to cart function

$(document).ready(function() {
    $(document).on('click', ".addtofirstcart", function() {
        // Get product details
        var aId = $(this).attr('data-address');
        var _vm = $(this);
        var productId = $(".productid-" + aId).val();
        var productTitle = $(".producttitle-" + aId).val();
        var quantity = $(".productquantity-" + aId).val();
        var selectedColor = $(".productcolor-" + aId).val();
        var selectedSize = $(".productsize-" + aId).val();
        var selectedPrice = $(".productprice-" + aId).val();

        console.log(aId, productId, productTitle, quantity, selectedColor, selectedSize, selectedPrice);

        // Remove the 'Ajax' line that was causing the error
        $.ajax({
            url: '/addtocart',
            data: {
                'id': productId,
                'qty': quantity,
                'title': productTitle,
                'price': selectedPrice,
                'color': selectedColor,
                'size': selectedSize
            },
            dataType: 'json',
            beforeSend: function() {
                _vm.attr('disabled', true);
            },
            success: function(res) {
                $("#cart-total").text(res.totalitems);
                // window.location.href = "/cart";
                console.log(res);
                _vm.attr('disabled', false);
            }
        });
    });
});




//for filter products 

    document.getElementById('toggleFilters').addEventListener('click', function() {
        document.querySelector('.filter-sidebar-mobile').style.display = 'block';
    });
    
    document.querySelector('.close-sidebar').addEventListener('click', function() {
        document.querySelector('.filter-sidebar-mobile').style.display = 'none';
    });




   