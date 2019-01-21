
$(document).ready(function(){

    // create Product, upload image feature
    const realFileBtn=document.getElementById("real-file");
    const customButton=document.getElementById("custom-button");
    const customText=document.getElementById("custom-text");

    customButton.addEventListener("click",function(){
        realFileBtn.click();

    });
    realFileBtn.addEventListener("change",function(){
        if (realFileBtn.value) {
            customText.innerHTML=realFileBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];

        }
        else{
            customText.innerHTML="No image Chosen yet !"
        }
    })

    // image delete button hover effect
    $(".ImageName .delBtn").hide();
    $( ".ImageName" ).hover(function() {
        $(".ImageName .delBtn").show()
    },function(){
        $(".ImageName .delBtn").hide()
    })


    $(".InventoryDetails").hide();
    $(".displayPD").click(function(){
        $(".InventoryDetails").hide();
        $(".productDetails").show('slow');
    })
    $(".displayPD+button").click(function(){
        $(".InventoryDetails").show('slow');
        $(".productDetails").hide();
    })

    // getting product id so we can delete it in a modal
    $("#DeleteProduct").on('show.bs.modal',function(event){
        
        button=$(event.relatedTarget)
        product_id=button.data('productid')
 
        modal=$(this)
        $(this).find(".modal-body .product_id").val(product_id);


    })
    $("#EditProduct").on('show.bs.modal',function(event){

        button=$(event.relatedTarget)
        product_id=button.data('editproductid')
 
        modal=$(this)
        $(this).find("#EditProductForm .edit_product_id").val(product_id);
       
        
    })
    

    
})