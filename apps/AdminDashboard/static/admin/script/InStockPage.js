
    // create Product, upload image feature
    const realFileBtn=document.getElementById("real-file");
    const customButton=document.getElementById("custom-button");
    const customText=document.getElementById("custom-text");

    if (customButton !=null) {
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
    }
    

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
    
    //------ In Stock Page ------
    $('#searchFormProduct').keyup(function(e) {
        e.preventDefault()
        $.ajax({
            method: "POST",
            url: $("#searchFormProduct").attr("action"),
            data: $('#searchFormProduct').serialize(),
            success: function(response) {
            console.log('received response:', response);
                
            $("#stocks").html(response)
        }

        });

    });

     //delete product
    $("#deleteProduct").submit(function(e){
        e.preventDefault();
       submitFormData($("#deleteProduct").serialize(),$("#deleteProduct").attr("action"));
       
    });
    function submitFormData(data,url){
        $.ajax({
            method:"POST",
            data:data,
            url:url,
            success:function(response){
                console.log('received response:', response);
                $("#stocks").html(response)
                $('.closebutton').click();

                
            }
        });
    }
    $(".editBTN").on("click",function(e){
        console.log("clicked")
        e.preventDefault();
        $.ajax({ 
            method:"GET",
            data:{
                product_id:$(this).data("editproductid")
            },
            url:$(this).attr("href"),
            success:function(response){
                console.log('received response:', response);
                $("#editInfo").html(response)
                const editrealFileBtn=document.getElementById("editreal-file");
                const editcustomButton=document.getElementById("editcustom-button");
                const editcustomText=document.getElementById("editcustom-text");
            
                editcustomButton.addEventListener("click",function(){
                    editrealFileBtn.click();
            
                });
                editrealFileBtn.addEventListener("change",function(){
                    if (editrealFileBtn.value) {
                        editcustomText.innerHTML=editrealFileBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
            
                    }
                    else{
                        editcustomText.innerHTML="No image Chosen yet !"
                    }
                })
            }
            
        });
       
    
    });
    // -----END OF in stock page -----