let getTotalPrice = () => {
    let total = 0;
    return fetch('/cart/total/')
    .then(response => response.json())
    .then(data => { 
        total += parseInt(data.total);
        return total;
    });
}

let updatePrice = () => {
    let total = getTotalPrice()
    //.then(response => response.text())
    .then(body => {
        // console.log(body);
        total = body;
        let totalEle = document.getElementById('cart-total');
        totalEle.innerHTML = `${total}`;
        totalEle = document.getElementById('total-after-discount');
        totalEle.innerHTML = `${total}`;
        totalEle = document.getElementById('total-price');
        // console.log(totalEle)
        if( totalEle != null){
            totalEle.innerHTML = `Total ${total}`;
        }
    });    
}


let removeItemId = (id) => {
    console.log("CLICKED");
    fetch('/cart/remove/' + id + '/', {
        method: 'POST',
    })
        .then(response => {
            // console.log(response);

            if(response.status === 200){
                // Remove the product from the cart;
                element = "#product_" + id;
                $(element).remove();
                updatePrice();
            }
        })
}

let increaseCount = (id) => {
    // console.log("Clicked "+ id);
    fetch('/cart/increase/' + id + '/', {
        method: "POST",
    })
    .then(response => response.json())
    .then(data => {
        if (data === 200){
            let ele = document.getElementById('quantity-'+id);
            ele.innerHTML = parseInt(ele.innerHTML) + 1;
            updatePrice();
        }else{
            alert('Error occured while increasing the quantity');
        }
    });
}

let decreaseCount = (id) => {
    // console.log("Clicked "+ id);
    let ele = document.getElementById('quantity-'+id);
    if(parseInt(ele.innerHTML) == "1"){
        removeItemId(id);
    }
    else{
        fetch('/cart/decrease/' + id + '/', {
            method: "POST",
        })
        .then(response => response.json())
        .then(data => {
            if (data === 200){
                let ele = document.getElementById('quantity-'+id);
                ele.innerHTML = parseInt(ele.innerHTML) - 1;
                updatePrice();
            }else{
                alert('Error occured while decreasing the quantity');
            }
        });
    }
}