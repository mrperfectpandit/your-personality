$(document).ready(function(){
    function renderServiceCards(data,pos){
        var serviceItem = $('<div>').attr({
            class : 'service-item',
            id : data.id
        })
        var h4 = $('<h4>').html(data.personality);
        var service = $('<div>').attr('class','service').append(h4);
        serviceItem.append(service);

        if(pos == 0){
            serviceItem.addClass('active-service');
            $('#service-image').attr('src',data.image);
            $('#name').html(data.name);
            $('#personality').html(data.personality);
            $('#description').html(data.description);
        }
        serviceItem.click(function(){
            $('.service-item').removeClass('active-service');
            serviceItem.addClass('active-service');
            $('#service-image').attr('src',data.image);
            $('#name').html(data.name);
            $('#personality').html(data.personality);
            $('#description').html(data.description);
        })

        return serviceItem;
    }
    $.get("https://60a4a320fbd48100179dc705.mockapi.io/project1/mbti",function(data){
        var countService = 0;
        var j = 1; 
        for(var i = 0;i<data.length;i++){
            if(countService < 2){
                $('#sc' + j).append(renderServiceCards(data[i],i));
                countService++ ;
            }
            else{
                countService = 1;
                j++;
                $('#sc' + j).append(renderServiceCards(data[i],i));
            }
        }
        console.log(data);
    })
})