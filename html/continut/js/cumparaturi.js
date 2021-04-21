inames=[];
icant=[];


function addItem(){
    inames.push(document.getElementById('pname').value)
    icant.push(parseInt(document.getElementById('pcant').value))

    displayCart()
}
function displayCart(){
    cartdata='<table><tr><th>Nr</th><th>Nume Produs</th><th>Cantitate</th></tr>';
    for(i=0;i<inames.length;i++){
        cartdata+="<tr><td>"+(i+1)+"</td><td>"+inames[i]+"</td><td>"+icant[i]+"</td><td><button onclick='delElement("+i+")'>Delete</button></td></tr>"

    }

    document.getElementById('cart').innerHTML=cartdata
    
}
function delElement(a){
    inames.splice(a,1);
    icant.splice(a,1)
    displayCart()
}
