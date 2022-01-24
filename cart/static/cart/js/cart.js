// let removeCartItemButtons = document.getElementsByClassName('remove-item');
// // console.log(removeCartItemButtons);

// for(var i=0; i<removeCartItemButtons.length; i++){
//     var button = removeCartItemButtons[i];
//     button.addEventListener('click', function(event){
//         var buttonClicked = event.target;
//         buttonClicked.parentElement.parentElement.remove();
//         updateCartTotal()
//     })
// }

// function updateCartTotal(){
//     var cartItemContainer = document.getElementsByClassName('items_container')[0];
//     var cartRows = cartItemContainer.getElementsByClassName('item_row');
//     for(var i=0; i<cartRows.length; i++){
//         var cartRow = cartRows[i];
//         var priceElement = cartRow.getElementsByClassName('cart-price')[0];
//         var quantityElement = cartRow.getElementsByClassName('cart-quantity')[0];
//         // console.log(priceElement, quantityElement);
//         var price = parseInt(priceElement.innerText);
//         var quantity = parseInt(quantityElement.innerText);
//         console.log(price * quantity);
//     }
// }

window.addEventListener("DOMContentLoaded", (event) => {
    cart = new Cart();
});

class Item{
    constructor(id, name, price, quantity, img) {
        if (typeof id === "object") {
          this.id = id.id;
          this.name = id.name;
          this.price = id.price;
          this.quantity = id.quantity;
          this.img = id.img;
        } else {
          this.id = id;
          this.name = name;
          this.price = price;
          this.quantity = quantity;
          this.img = img;
        }
    }
    get total() {
        return parseInt(this.price, 10) * parseInt(this.quantity, 10);
    }
}

class Cart{
    getFromLS() {
        let raw_data = localStorage.getItem("cart_items");
        if(raw_data) return JSON.parse(raw_data);
        return {};
    }

    constructor(){
        this.container = document.getElementById('items_container');
        this.summaryContainer = document.getElementById('s_container');
        this.items = {}
        this.savedItems = this.getFromLS();
        this.addCartUrl = '/cart/add/';
        this.removeCartUrl = '/cart/remove';
        for(let item in this.savedItems){
            this.addItem(new Item(this.savedItems[item]));
        }
        this.save();
    }

    save(){
        let cartTotal = document.getElementById('cart-total');
        // cartTotal.innerHTML = "Rs. ${this.total}";
        localStorage.setItem('cart_items', JSON.stringify(this.items));
    }

    addToDom(item){
        this.container.innerHTML += `
            <div class="row mt-5 item_row" id='item-${item.id}'>
                <div class="col-3"><img src="${item.img}" alt="" class="i_img"></div>
                <div class="col-5">
                    <div class="t2">${this.name}</div>
                    <div class="o_inc mt-3"><span class="for">Qty</span>
                        <button data-id='${item.id}' data-quantity='${item.quantity}' class="minus" onClick="decreaseQuantity(event)">-</button>
                        <div class="num cart-quantity">${item.quantity}</div>
                        <button data-id='${item.id}' data-quantity='${item.quantity}' class="plus" onClick="increaseQuantity(event)">+</button>
                    </div>
                </div>
                <div class="col-4">
                    <div class="t2">Price - <span class='cart-price'>${item.total}</span></div>
                    <div class="t2 mt-5 remove-item" onClick="cart.removeItem(${item.id})">REMOVE</div>
                </div>
            </div>
        `
        // Summary container is remaining
    }

    removeFromDom(item_id){
        let ele = document.getElementById(`item-${item_id}`);
        if(ele) ele.remove();
    }

    addItem(item){
        if (item instanceof Item){
            this.items[item.id] = item;
            this.save();
            this.removeFromDom(item.id);
            this.addToDom(item);
        }
    }

    removeItem(id){
        delete this.item[id];
        this.removeFromDom(id);
        this.save();
    }

    get total(){
        let total = 0;
        for(let item in this.items){
            total += parseInt(this.items[item].total, 10)
        }
        return total;
    }
}

let cart;

let addToCart = (e) => {
    // console.log(e.target.dataset);
    dataset = e.target.dataset;
    stock = dataset.stock;
    if(stock < 1){
        alert('Out of stock');
        return;
    }
    let item = new Item(
        dataset.id,
        dataset.name,
        dataset.price,
        1,
        dataset.img
    );
    cart.addItem(item);
}

let removeFromCart = (e) => {
    console.log(e.target.dataset);
    let itemId = e.target.dataset.targetid;
    console.log(itemId);
    if(itemID) cart.removeItem(itemId);
}

const increaseQuantity = (e) => {
    let id = e.target.dataset.id;
    oldItem = cart.items[id];
    oldItem.quantity++;
    cart.addItem(oldItem);
}

const decreaseQuantity = (e) =>{
    id = e.target.dataset.id;
    oldItem = cart.items[id];
    if(oldItem.quantity > 1){
        oldItem.quantity--;
        cart.addItem(oldItem);
    }
    cart.addItem(oldItem);
}