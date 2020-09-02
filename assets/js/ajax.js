// $(document).ready(function(){
// Codes for Ajax
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            setLoader()
        }
    });

    var $myForm = $('.my-ajax-form')
    $myForm.submit(function(event){
        event.preventDefault()
        resetForm()
        var $formData = $(this).serialize()
        var $thisURL = $myForm.attr('data-url') || window.location.href // or set your own url
        $.ajax({
            method: "POST",
            url: $thisURL,
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError,
            complete: destroyLoader,
        })
    })

    function callComo(data, textStatus, jqXHR) {
        destroyLoader()
    }

    function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data)
        console.log(textStatus)
        console.log(jqXHR)
        ajaxListener(jqXHR.responseJSON, textStatus)
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR)
        ajaxListener(jqXHR.responseJSON, textStatus)
        console.log(textStatus)
        console.log(errorThrown)
    }
// });