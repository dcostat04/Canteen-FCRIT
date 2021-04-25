
let carts=document.querySelectorAll('.add-cart');
let remove=document.querySelectorAll('.remove');
let decerease=document.querySelectorAll('.decerease');
let inc=document.querySelectorAll('.products');

let products=[
	{
		name:'frankie',
		cost:30,
		inCart:0
	},
	{
		name:'haka noodles',
		cost:80,
		inCart:0
	},
	{
		name:'Manchurian',
		cost:30,
		inCart:0
	},
	{
		name:'Veg. Fried Rice',
		cost:120,
		inCart:0
	}
	]

for(let i=0;i<carts.length;i++){
	carts[i].addEventListener('click',()=>{cartNum(products[i]);
		totalCost(products[i]);})
}
for(let i=0;i<2;i++){
	inc[i].addEventListener('click',()=>{cartNum(products[i]);
		totalCost(products[i]);})
}
function onLoadCartNum(){
	let productNum=localStorage.getItem('cartNum');
	if(productNum){
		document.querySelector('.nav-link span').textContent =productNum;
		}
	}

function cartNum(product){

	let productNum=localStorage.getItem('cartNum');
	productNum=parseInt(productNum);
	if(productNum){
		localStorage.setItem('cartNum',productNum+1);
		document.querySelector('.nav-link span').textContent =productNum + 1;
		}
	
	else{
		localStorage.setItem('cartNum',1);
	     document.querySelector('.nav-link span').textContent =1;
	     }
	setItems(product);     
}
function setItems(product){
	let cartItems=localStorage.getItem('productsInCart');
	cartItems=JSON.parse(cartItems);
	console.log("my cartItems are:",cartItems);
	if(cartItems!=null){
		if(cartItems[product.name]==undefined){
			cartItems={
				...cartItems,
				[product.name]:product
			}
		}
		cartItems[product.name].inCart+=1;
	}else{
	product.inCart=1;
	cartItems={[product.name]:product}
	}
	localStorage.setItem("productsInCart",JSON.stringify(cartItems));
}

function totalCost(product){
	//console.log("the product price is:",product.cost);
	let cartCost=localStorage.getItem('totalCost');
	
	console.log("my cart cost is",cartCost);
	if(cartCost!=null){
		cartCost=parseInt(cartCost);
		localStorage.setItem("totalCost",cartCost + product.cost);
	}
		else{
	localStorage.setItem("totalCost",product.cost);}
}

function displayCart(){
	let cartItems=localStorage.getItem("productsInCart");
	cartItems= JSON.parse(cartItems);
	let productContainer=document.querySelector(".products");
		let cartCost=localStorage.getItem('totalCost');

	if(cartItems && productContainer){
		productContainer.innerHTML='';
		Object.values(cartItems).map(item=>{productContainer.innerHTML +=`
			
			<div class="product">
			     <ion-icon class="remove" name="close-circle-outline"></ion-icon>
			 	<span>${item.name}</span>
			 </div>
			 <div class="price">Rs.${item.cost}/-</div>
			 
			 <div class="quantity">	<ion-icon class="decrease" name="chevron-back-circle-outline"></ion-icon>
			 	<span>${item.inCart}</span>
			 	<a class="increase" href="#"><ion-icon name="chevron-forward-circle-outline"></ion-icon></a>
			 </div>
			<div class="total">Rs.${item.inCart*item.cost}/-</div>
			 `;		});
		productContainer.innerHTML+=`
			<div class="totalCartContainer">
				<h4 class="totalTitle">
				Cart Total
				</h4>
				<h4 class="totalCart">
					Rs.${cartCost}/-	
				</h4>
		`;

	}
}
onLoadCartNum();
displayCart();