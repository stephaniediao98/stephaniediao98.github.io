var classes = $('#classes');
// var class_ids = [178627]

$.ajax ({
    url: 'http://api.asg.northwestern.edu/courses/details/',
    data: {
        key: 'TwewRiLaO2UQkhVw',
        id: 178620,
        // id: 178627,
        // id: 178611,
        // id: 178608,
    },
    type: 'GET',
    dataType: 'json',

    error: function(xhr, status, error){
        var errorMessage = xhr.status + ': ' + xhr.statusText;
        alert('Error - ' + errorMessage);
        },

    success: function(data) { 
        $.each(data, function(index, item) { 
            classes.append('<h3>' + item.title + '</h3><br>');
        });
    }
})
