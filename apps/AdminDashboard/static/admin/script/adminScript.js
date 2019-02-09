
$(document).ready(function(){

// -----Admin Dashboard-----
    $( ".OrderStatus" ).on("change",function() {
        console.log("chnage")
        var form=$(this).parent()
        console.log(form)
        console.log($(form).attr("action"))

       
        $.ajax({
            method:"POST",
            url:$(form).attr("action"),
            data:$(form).serialize(),
            success:function(response){
                console.log(response);
            }
        })
        // data:{"select":$(this).val(),"orderId": $(this).find('option:selected').attr("data-orderId"),csrfmiddlewaretoken: '{{ csrf_token }}'},
    
    })
    
    $('#searchFormOrderList').on("keyup", function(e) {
        e.preventDefault()
        $.ajax({
           method: "POST",
           url: $("#searchFormOrderList").attr("action"),
           data: $('#searchFormOrderList').serialize(),
           success: function(response) {
            console.log('received response:', response);
                
           $("#orderlist").html(response)
        }

        });

    });
// -----End Admin Dashboard-----




    
})