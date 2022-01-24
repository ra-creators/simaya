class Item{
    constructor(id, name, price, quantity, image){
        if (typeof id === 'object'){
            this.id = id.id;
            this.name = id.name;
            this.price = id.price;
            this.quantity = parseInt(id.quantity, 10);
            this.img = id.img;
        }else{
            this.id = id;
            this.name = name;
            this.price = price;
            this.quantity = parseInt(quantity, 10);
            this.img = img;
        }
    }

    get total(){
        return parseInt(this.price, 10) * parseInt(this.quantity, 10);
    }
}

class Cart{
    constructor(cartDetails = false){
        
    }
}